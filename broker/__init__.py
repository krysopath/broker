#!/usr/bin/env python3
# coding=utf-8
from json import dumps

from flask import Flask, make_response
from flask_httpauth import HTTPBasicAuth
from flask_restful import Api

from .config import __dbconn__

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = __dbconn__
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
auth = HTTPBasicAuth()

from broker.database import db_session, init_db
from broker.models import *
from broker.models.user_func import *
from broker.ressources import UsersList, GetToken, UserRessource
from broker.jsonize import APIEncoder
from broker.exceptions import *
from broker.util import verify_password


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


init_db()

api = Api(app, errors=errors)
api.add_resource(UsersList, '/api/v2/users')
api.add_resource(UserRessource, '/api/v2/users/<string:user_name>')
api.add_resource(GetToken, '/api/v2/token')


@api.representation('application/json')
def output_json(data, code, headers=None):
    resp = make_response(
        dumps(
            data,
            cls=APIEncoder,
            indent=2
        ),
        code
    )
    resp.headers.extend(headers or {})
    return resp


@auth.verify_password
def verify_pw(username_or_token, password):
    try:
        return verify_password(username_or_token, password)
    except RuntimeWarning as rtw:
        return False
