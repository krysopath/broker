#!/usr/bin/env python3
# coding=utf-8
from flask import Flask
from flask_restful import Api

from .config import __dbconn__

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = __dbconn__
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from broker.database import db_session, init_db
from broker.models import *
from broker.models.user_func import *
from broker.ressources.users_ressources import UsersAPI
from broker.jsonize import jsonize
from broker.exceptions import *


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


init_db()
print(type(User))
print(type(User()))

api = Api(app, errors=errors)
api.add_resource(UsersAPI, '/api/v1/users')
# api.add_resource(UserAPI, '/api/v1/users/<user_name>')
