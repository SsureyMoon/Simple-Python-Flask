# Simple-Python-App

Simple project in Python, SQLAlchemy, and Flask

## How it works

1. HTTP requests and responses are handled by Flask web framework.
2. JSON Web Token is used to authenticate and authorize users.
3. SQLAlchemy with SQLite is used to store data.
4. Tornado is used as a web server.
5. Facebook and Google + OAuth 2.0 are used 

## Main dependencies
- [Python](https://www.python.org/) version 2.7.x or higher
- [Flask](http://flask.pocoo.org/) version 0.10.x or higher
- [Jinja2](http://jinja.pocoo.org/docs/dev/) 2.7.x or higher
- [SQLAlchemy](http://www.sqlalchemy.org/) 0.8.x or higher
- [PyJWT](https://github.com/jpadilla/pyjwt) 1.3.x or higher
- [Tornado](http://www.tornadoweb.org/en/stable/) 4.x or higher
- [Oauth2.0client](https://developers.google.com/api-client-library/python/guide/aaa_oauth) 1.4.x or higher 


## Getting Started
### Setting Environment

#### Cloning the source code.
```bash
git clone https://github.com/SsureyMoon/Simple-Python-Flask.git
```

#### Installing python depedencies
We use [pip]((https://pip.pypa.io/en/latest/installing.html)) to install python dependencies.
Using [virtual environment](https://virtualenv.pypa.io/en/latest/) is stronly recommended.
```bash
cd /where/your/project/root/is
pip install -r requirements.txt
```

#### Install front-end depedencies
We use [Bower](http://bower.io/) to install front-end dependcies.
```bash
cd catalog_app
bower update
```

### Importing dummy data
```bash
cd /where/your/project/root/is
python testdata.py
```
Now, we can login with username: user{i}@email.com, password: user{i}password.
For example, username: ```user1@email.com```, password: ```user1password```

### Download a credentials file
For Google Plus Oauth, we need to download google api credential file.
Visit your developer console and downlaod credentials.json.
The url must look like this:

https://console.developers.google.com/project/your-app-name/apiui/credential

Place the json file dowloaded in the folder ```catalog_app/settings/```


## Run and test the server
```bash
python runserver.py
```
Test your application by visiting http://localhost:8000.