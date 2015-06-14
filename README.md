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

### Setting the basic environment (Ubuntu 14.04)
```bash
sudo apt-get install build-essential
sudo apt-get install update
sudo apt-get install upgrade
sudo apt-get install git python-dev python-setuptools python-pip

```

### Cloning the source code.
```bash
git clone https://github.com/SsureyMoon/Simple-Python-Flask.git
```

### Installing python dependencies
We use [pip]((https://pip.pypa.io/en/latest/installing.html)) to install python dependencies.
Using [virtual environment](https://virtualenv.pypa.io/en/latest/) is strongly recommended.
```bash
cd /where/your/project/root/is
pip install -r requirements.txt
```

### Installing front-end dependencies
#### Installing Bower
Bower requires Node.js. Please visit [here](https://Nodejs.org/), download and install Node.js.
Install Bower by Node.js
```bash
npm install -g bower
```
#### Installing front-end libraries
Install front-end libraries with [Bower](http://bower.io/)
```bash
cd catalog_app
bower update
```

### Downloading a credentials file for Google + OAuth
For Google Plus Oauth, we need to download google api credential file.
Visit your developer console and downlaod credentials.json.
The ```url``` must look like this:

https://console.developers.google.com/project/**your-app-name**/apiui/credential

Place the ```client_secret.json``` file downloaded in the folder ```catalog_app/settings/```

### Setting credentials for Facebook OAuth
Open ```catalog_app/settings/config.py```, find these lines:
```python
# Replace this with your facebook client id.
FACEBOOK_CLIENT_ID = ""
# Replace this with your facebook client secret.
FACEBOOK_CLIENT_SECRET = ""
```
Visit your Facebook developer page and go to the settings tab.
The ```url``` must look like this:

https://developers.facebook.com/apps/**your-app-id**/settings/basic/
Find ```App ID``` and ```App Secret``` and fill the blanks inthe ```catalog_app/settings/config.py```

** Please NEVER commit your code with your app secret! You can avoid that by running this command: **
```bash
cd /where/your/project/root/is
echo 'catalog/settings/config.py' >> .gitignore
```

### Importing dummy data
```bash
cd /where/your/project/root/is
python testdata.py
```
Now, we can login with username: user{i}@email.com, password: user{i}password.
For example, username: ```user1@email.com```, password: ```user1password```

## Run and test the server
```bash
python runserver.py
```
Test your application by visiting http://localhost:8000.