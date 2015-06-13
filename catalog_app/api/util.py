import hashlib
import hmac
import string
import random
import uuid
import json
from base64 import b64encode, urlsafe_b64encode
from datetime import datetime, timedelta
import settings.config
import time
import jwt


def encrypt_password(password):
    salt = uuid.uuid4().hex
    encrypted_password = hashlib.sha256(password.encode('utf-8')+salt).hexdigest()
    return encrypted_password, salt

def check_password(password, encrypted_password, salt):
    return encrypted_password == \
            hashlib.sha256(password.encode('utf-8') + salt).hexdigest()

def generate_token(user):
    header = {
        "type": "JWT",
        "hash": "SHA256"
    }
    expire_time = int(time.time())+ 3600
    payload = {
        'exp': expire_time, # one hour
        'username': user.name,
        'id': user.id
    }
    secret = settings.config.SECRET_KEY
    signature = jwt.encode(payload=payload, key=secret,
                           algorithm='HS256', headers=header)
    return expire_time, signature

def validate_token(token, expire_time):
    if int(time.time()) > int(expire_time):
        # token expired
        return False
    secret = settings.config.SECRET_KEY
    try:
        result = jwt.decode(jwt=token, key=secret, algorithms='HS256')
        return result
    except:
        return False
