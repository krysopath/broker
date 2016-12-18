#!/usr/bin/env python3
# coding=utf-8
from flask_restful import Resource

from broker import auth
from broker.database import db_session as db
from broker.models import get_all_users, User
from broker.parser import user_parser


class UsersList(Resource):
    decorators = [auth.login_required]
    parser = user_parser

    def get(self):
        result = {user.id: user
                  for user in get_all_users()}

        return {
            "action": "get_all_users",
            "result": {
                "users": result or None
            }
        }

    def post(self):
        args = self.parser.parse_args()
        check = User.query.filter(
            User.name == args['name']
        ).first()

        if not check:
            user = User()
            for k, v in args.items():
                if v != None:
                    setattr(user, k, v)
            db.add(user)
            db.commit()

            return {
                "action": "add_user",
                "result": {
                    "id": user.id,
                    "name": user.name
                }
            }


class UserRessource(Resource):
    decorators = [auth.login_required]
    parser = user_parser

    def get(self, user_name):
        results = {}
        user = User.query.filter(User.name == user_name).first()
        if user:
            results = {'user': user}

        return {
            'action': 'get_user',
            'result': None or results
        }

    def put(self, user_name):
        def answer():
            return {
                "action": "update_user",
                "name": user_name,
                "result": changes or None
            }

        args = self.parser.parse_args()
        user = User.query.filter(
            User.name == user_name).first()
        changes = {}
        if user:
            for k, v in args.items():
                if v:
                    setattr(user, k, v)
                    changes[k] = v

            db.commit()
            return answer()

        else:
            return answer()

    def delete(self, user_name):
        def answer(result):
            return {
                "action": "del_user",
                "result": {
                    "id": user.id or None,
                    "name": user.name,
                    "deleted": result
                }
            }

        user = User.query.filter(User.name == user_name).first()
        if user:
            db.delete(user)
            db.commit()
            return answer(True)

        else:
            return answer(False)
