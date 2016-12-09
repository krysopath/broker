#!/usr/bin/env python3
# coding=utf-8
from os import mkdir, environ
from os.path import exists
from flask import Flask, jsonify, g, request, make_response
from flask_restful import Resource, Api, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from exceptions import *
from functools import wraps
from flask import request, Response

__home__ = '{}//'.format(environ['HOME'])
__dbfile__ = __home__ + 'broker.db'
__dbconn__ = 'sqlite:///{}'.format(__dbfile__)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = __dbconn__
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app, errors=errors)
db = SQLAlchemy(app)


def check_auth(username, password):
    return username == 'g' and password == 'g25v09e85'


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


class User(db.Model):
    id = db.Column(db.Integer, db.Sequence('user_id_seq'), primary_key=True)
    name = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(50))
    fullname = db.Column(db.String(100), nullable=True)
    group = db.Column(db.String(100))
    rank = db.Column(db.Integer)
    hash = db.Column(db.String(512))
    creation_time = db.Column(
        db.TIMESTAMP, server_default=db.func.current_timestamp(),
        nullable=False
    )

    def __repr__(self):
        return "<User(id='%s', name='%s', email='%s')>" \
               % (self.id, self.name, self.email)

    def __iter__(self):
        for p in ['id', 'name', 'email', 'fullname', 'group', 'rank', 'creation_time']:
            yield p, getattr(self, p)

parser = reqparse.RequestParser()
parser.add_argument('name', type=str)
parser.add_argument('email', type=str)
parser.add_argument('fullname', type=str)
parser.add_argument('group', type=str)
parser.add_argument('rank', type=int)



class UsersAPI(Resource):
    @requires_auth
    def get(self):
        users = db.session.query(User).order_by(User.id).all()
        results = {}

        for user in users:
            results[user.id] = dict(user)

        return jsonify(results)

    @requires_auth
    def post(self):
        args = parser.parse_args()
        check = db.session.query(User).filter(
                        User.name == args['name']).first()
        if not check:
            user = User()
            user.name = args['name']
            user.email = args['email']
            user.group = args['group']
            user.fullname = args['fullname']
            user.rank = args['rank']

            db.session.add(user)
            db.session.commit()

            return jsonify(dict(user))

        else:
            raise UserAlreadyExistsError


class UserAPI(Resource):
    @requires_auth
    def get(self, user_name):
        user = db.session.query(User)\
            .filter(User.name == user_name)\
            .first()
        results = {'data': dict(user)}

        return jsonify(results)

    @requires_auth
    def put(self, user_name):
        if not str(user_name) == user_name:
            raise MalformedPost
        args = parser.parse_args()
        user = db.session.query(User).filter(
            User.name == user_name).first()
        if user:
            changes = {}
            for k, v in args.items():
                if v:
                    setattr(user, k, v)
                    changes[k] = v

            db.session.commit()
            return jsonify({'changes': changes})
        else:
            return jsonify({'changes': None})

    @requires_auth
    def delete(self, user_name):
        if not str(user_name) == user_name:
            raise MalformedPost
        user = db.session.query(User).filter(
            User.name == user_name).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return jsonify({'deleted': user_name})
        else:
            return jsonify({'changes': None})


db.create_all()
api.add_resource(UsersAPI, '/api/v1/users')
api.add_resource(UserAPI, '/api/v1/users/<user_name>')


if __name__ == '__main__':
    context = ('certs/broker.crt',
               'certs/broker.key')
    app.run(
        host='0.0.0.0',
        port=4444,
        ssl_context=context,
        threaded=True,
        debug=True)

