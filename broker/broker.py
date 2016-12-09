#!/usr/bin/env python3
# coding=utf-8

from flask import jsonify
from flask_restful import Resource, Api

from util import requires_auth
from parser import user_parser
from model import db, app, User
from exceptions import *


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
        args = user_parser.parse_args()
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
        args = user_parser.parse_args()
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
            return jsonify({'deleted': None})


db.create_all()
api = Api(app, errors=errors)
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

