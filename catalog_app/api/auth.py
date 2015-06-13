import json

import httplib2
import requests

from flask import render_template, request, Blueprint, \
    redirect, url_for, flash, make_response
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError

from catalog_app import session
from catalog_app.api.models import User
from util import check_password, encrypt_password, generate_token


CLIENT_ID = json.loads(
    open('settings/client_secret.json', 'r').read())['web']['client_id']

auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('/login/', methods=['GET', 'POST'])
def login(cached_email=None):
    if request.method == 'GET':
        return render_template('login.html', cached_email=cached_email)

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if not (email and password):
            flash("Please fill the form. ")
            return render_template('login.html', cached_email=email)
        user = User.get_by_email(session, email.strip())
        if not user:
            flash("Invalid email address or password. ")
            return render_template('login.html', cached_email=email)
        if not user.password:
            flash("You've signed up with social service. ")
            return render_template('login.html', cached_email=email)
        if not check_password(password, user.password, user.salt):
            flash("Invalid email address or password. ")
            return render_template('login.html', cached_email=email)
        expire_time, token = generate_token(user)
        response = make_response(redirect(url_for('api.showMain')))
        response.set_cookie('token', value=token)
        response.set_cookie('expire_time', value=str(expire_time))
        return response


@auth.route('/signup/', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        if not (email and password and confirm):
            flash("Please fill the form. ")
            return render_template('signup.html', cached_email=email)
        if not (password == confirm):
            flash("Confirm password has to be the same as password")
            return render_template('signup.html', cached_email=email)
        user = User.get_by_email(session, email.strip())
        if user:
            if user.password:
                flash("Such user already exist. Please login")
                return render_template('signup.html', cached_email=email)
        else:
            user = User(email=email.strip())
        user.password, user.salt = encrypt_password(password)
        session.add(user)
        session.commit()
        expire_time, token = generate_token(user)
        response = make_response(redirect(url_for('api.showMain')))
        response.set_cookie('token', value=token)
        response.set_cookie('expire_time', value=str(expire_time))
        return response


@auth.route('/gconnect/', methods=['POST'])
def gconnect():
    code = request.data
    try:
        oauth_flow = flow_from_clientsecrets('settings/client_secret.json',
                                             scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        flash("Google plus connection Error.")
        response = make_response(json.dumps('Fail to upgrade'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = credentials.access_token
    url = ('https://www.googleapis.'
           'com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    if result.get('error') is not None:
        flash("Google plus connection Error.")
        response = make_response(
            json.dumps(result.get('error')), 500
        )
        response.headers['Content-Type'] = 'application/json'
        return response

    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        flash("Google plus connection Error.")
        response = make_response(
            json.dumps("Token's user ID doesn't match"), 401
        )
        response.headers['Content-Type'] = 'application/json'
        return response

    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID doesn't match"), 401
        )
        flash("Google plus connection Error.")
        response.headers['Content-Type'] = 'application/json'
        return response

    userinfo_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = json.loads(answer.text)
    email = data['email']
    user = User.get_by_email(session, email.strip())

    if not user:
        user = User(email=email)

    session.add(user)
    session.commit()

    flash("Successfully logged in with Google +")
    expire_time, token = generate_token(user)
    response = make_response(redirect(url_for('api.showMain')))
    response.set_cookie('token', value=token)
    response.set_cookie('expire_time', value=str(expire_time))
    response.set_cookie('gplus_token', value=access_token)

    return response


@auth.route('/gdisconnect', methods=['GET'])
def gdisconnect():
    access_token = request.cookies.get('gplus_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user is not connected.'), 200
        )
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        response = make_response(
            json.dumps('Successfully disconnected'), 200
        )
        response.set_cookie('gplus_token', '', expires=0)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user'), 400
        )
        response.headers['Content-Type'] = 'application/json'
        return response


@auth.route('/fconnect/', methods=['POST'])
def fconnect():
    userinfo = json.loads(request.data)
    print userinfo
    email = userinfo.get('email')
    user = User.get_by_email(session, email.strip())

    if not user:
        user = User(email=email)
        session.add(user)
        session.commit()

    expire_time, token = generate_token(user)
    flash("Successfully logged in with Facebook")
    response = make_response(redirect(url_for('api.showMain')))
    response.set_cookie('token', value=token)
    response.set_cookie('expire_time', value=str(expire_time))
    return response


@auth.route('/logout/')
def logout():
    token = request.cookies.get('token')
    response = make_response(
        json.dumps("Successfully logged out"), 200
    )
    if not token:
        response = make_response(
            json.dumps("You've already logged out"), 200
        )

    flash("Successfully logged out.")
    response.set_cookie('token', '', expires=0)
    response.set_cookie('expire_time', '', expires=0)
    return response
