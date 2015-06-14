import os


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'catalog.db')

# Replace this secret key with your unique super secret.
SECRET_KEY = "super secret nyan cat"

JWT_EXPIRE = 60 * 60

# Replace this with your facebook client id.
FACEBOOK_CLIENT_ID = ""
# Replace this with your facebook client secret.
FACEBOOK_CLIENT_SECRET = ""
