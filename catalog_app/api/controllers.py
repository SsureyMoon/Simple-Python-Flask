from flask import render_template, Blueprint, request,\
    redirect, url_for, flash, jsonify

from catalog_app import session
from catalog_app.api.models import User, Category, Item
from util import validate_token


root = Blueprint('root', __name__)
api = Blueprint('api', __name__, url_prefix="/api")


@root.route('/')
@api.route('/')
def showMain():
    token = request.cookies.get('token')
    expire_time = request.cookies.get('expire_time')
    user_data = None
    if token:
        user_data = validate_token(token, expire_time)
    categories = Category.get_all(session, order_by=Category.name,
                                  ascending=True)
    items = Item.get_recent(session, limit=10)
    return render_template('main.html', categories=categories,
                           items=items, user=user_data)


@api.route('/category/<int:category_id>/')
def showItemList(category_id):
    token = request.cookies.get('token')
    expire_time = request.cookies.get('expire_time')
    user_data = None
    if token:
        user_data = validate_token(token, expire_time)
    categories = Category.get_all(session, order_by=Category.created,
                                  ascending=True)
    category = Category.get_by_id(session, category_id)
    if category:
        items = Category.item_set(session, category.id)
    else:
        items = []
    return render_template('show_item_list.html', categories=categories,
                           category=category, items=items, user=user_data)


@api.route('/category/<int:category_id>/item/<int:item_id>')
def showItemDetail(category_id, item_id):
    token = request.cookies.get('token')
    expire_time = request.cookies.get('expire_time')
    user_data = None
    if token:
        user_data = validate_token(token, expire_time)
    category = Category.get_by_id(session, category_id)
    item = Item.get_by_id(session, item_id)
    return render_template('show_item_detail.html',
                           category=category, item=item, user=user_data)


@api.route('/items/', methods=['GET', 'POST'])
def addItem():
    token = request.cookies.get('token')
    expire_time = request.cookies.get('expire_time')
    if request.method == "GET":
        if not token:
            flash("Please login.")
            return redirect(url_for('api.showMain'))

        user_data = validate_token(token, expire_time)
        if not user_data:
            flash("Please login.")
            return redirect(url_for('api.showMain'))

        categories = Category.get_all(session)
        return render_template('add_item.html',
                               categories=categories, user=user_data)

    if request.method == "POST":
        if not token:
            flash("Please login.")
            return redirect(url_for('api.showMain'))

        user_data = validate_token(token, expire_time)
        if not user_data:
            flash("Please login.")
            return redirect(url_for('api.showMain'))

        title = request.form.get('title')
        description = request.form.get('description')
        category_id = request.form.get('category')
        if not title:
            flash("Please fill the form.")
            return redirect(url_for('api.addItem'))

        item = Item(title=title, description=description,
                    category_id=category_id, user_id=user_data.get("id"))
        session.add(item)
        session.commit()
        flash("The item was successfully created.")
        return redirect(url_for('api.showItemDetail',
                                category_id=category_id, item_id=item.id))


@api.route('/category/<int:category_id>/item/<int:item_id>/edit',
           methods=['GET', 'POST'])
def editItem(category_id, item_id):
    token = request.cookies.get('token')
    expire_time = request.cookies.get('expire_time')
    if request.method == "GET":
        if not token:
            flash("You are not authorized.")
            return redirect(url_for('api.showMain'))

        user_data = validate_token(token, expire_time)

        if not user_data:
            flash("You are not authorized.")
            return redirect(url_for('api.showMain'))

        if not User.is_authorized(session, user_data.get("id"), item_id):
            flash("You are not authorized.")
            return redirect(url_for('api.showMain'))

        categories = Category.get_all(session)
        item = Item.get_by_id(session, item_id)
        return render_template('edit_item.html',
                               categories=categories, item=item)

    if request.method == "POST":
        if not token:
            flash("You are not authorized.")
            return redirect(url_for('api.showMain'))

        user_data = validate_token(token, expire_time)
        if not user_data:
            flash("You are not authorized.")
            return redirect(url_for('api.showMain'))

        category_id = request.form.get('category')

        if not User.is_authorized(session, user_data.get("id"), item_id):
            flash("You are not authorized.")
            return redirect(url_for('api.showMain'))

        item = Item.get_by_id(session, item_id)

        title = request.form.get('title')
        description = request.form.get('description')
        new_category_id = request.form.get('category')

        if not title:
            flash("You are not authorized.")
            return redirect(url_for('api.addItem'))

        item.title = title
        item.description = description
        item.category_id = new_category_id
        print item.category_id
        print item.category_id
        print item.category_id


        session.add(item)
        session.commit()
        flash("The item was successfully updated.")
        return redirect(url_for('api.showItemDetail',
                                category_id=category_id, item_id=item.id))


@api.route('/item/<int:item_id>/delete/', methods=['GET', 'POST'])
def deleteItem(item_id):
    token = request.cookies.get('token')
    expire_time = request.cookies.get('expire_time')
    if request.method == "GET":
        if not token:
            flash("You are not authorized.")
            return redirect(url_for('api.showMain'))

        user_data = validate_token(token, expire_time)

        if not user_data:
            flash("You are not authorized.")
            return redirect(url_for('api.showMain'))

        item = Item.get_by_id(session, item_id)
        return render_template('delete_item.html', item=item, user=user_data)

    if request.method == "POST":
        if not token:
            flash("You are not authorized.")
            return redirect(url_for('api.showMain'))

        user_data = validate_token(token, expire_time)
        if not user_data:
            flash("You are not authorized.")
            return redirect(url_for('api.showMain'))

        user = User.get_by_id(session, user_data.get("id"))

        if not User.is_authorized(session, user.id, item_id):
            flash("You are not authorized.")
            return redirect(url_for('api.showMain'))

        item = Item.get_by_id(session, item_id)

        session.delete(item)
        session.commit()
        flash("The item was successfully deleted")
        return redirect(url_for('api.showMain'))


# JSON end point
@api.route('/catalog.json')
def getAllContent():
    categories = Category.get_all(session, order_by=Category.name,
                                  ascending=True)
    categories_list = [c.serialize for c in categories]
    for c in categories_list:
        c["items"] = [i.serialize for i in Category.item_set(session, c["id"])]
    result = {
        "status": "success",
        "type": "collection",
        "collection_type": "categories",
        "categories": categories_list
        }
    return jsonify(result)


@api.route('/category/<int:category_id>/item.json')
def getJsonItemList(category_id):
    category = Category.get_by_id(session, category_id)
    if category:
        items = Category.item_set(session, category.id)
    else:
        items = []

    result = {
        "status": "success",
        "type": "collection",
        "collection_type": "items",
        "category": category.serialize,
        "items": [i.serialize for i in items]
        }
    return jsonify(result)


@api.route('/category/<int:category_id>/item/<int:item_id>/detail.json')
def getJsonItemDetail(category_id, item_id):
    category = Category.get_by_id(session, category_id)
    item = Item.get_by_id(session, item_id)
    result = {
        "status": "success",
        "type": "attributes",
        "attributes_type": "item",
        "category": category.serialize,
        "item": item.serialize
    }
    return jsonify(result)
