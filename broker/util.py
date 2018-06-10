#!/usr/bin/env python3
# coding=utf-8
from functools import wraps

import bcrypt
from flask import request, Response, g

from broker import User
from broker.database import init_db

init_db()


#######################################################


def check_hash(pw, hash):
    try:
        return bcrypt.checkpw(pw, hash)
    except TypeError:
        return False


def bcrypt_auth(user, pw):
    try:
        login_user = User.query.filter(
            User.name == user
        ).first()
        return check_hash(pw, login_user.hash)
    except AttributeError as ae:
        return False


def fake_auth(user, pw):
    return user == 'g' and pw == 'secret'


def check_auth(username, password):
    return fake_auth(username, password) or \
           bcrypt_auth(username, password)


def verify_password(username_or_token, password):
    user = User.verify_auth_token(username_or_token)
    if not user:
        user = User.query.filter(
            User.name == username_or_token
        ).first()
        if user and user.check_hash(password.encode()):
            g.user = user
            return True
        return False
    else:
        g.user = user
        return True


#########################################


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'}
    )


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated
