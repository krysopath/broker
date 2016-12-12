#!/usr/bin/env python3
# coding=utf-8
from json import dumps

from flask import Flask, make_response
from flask_restful import Api

from .config import __dbconn__

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = __dbconn__
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from broker.database import db_session, init_db
from broker.models import *
from broker.models.user_func import *
from broker.ressources.users_ressources import UsersAPI
from broker.jsonize import APIEncoder
from broker.exceptions import *


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


init_db()

api = Api(app, errors=errors)
api.add_resource(UsersAPI, '/api/v1/users')
# api.add_resource(UserAPI, '/api/v1/users/<user_name>')


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
