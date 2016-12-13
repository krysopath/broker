#!/usr/bin/env python3
# coding=utf-8
from flask_restful import Resource

from broker import auth
from broker.database import db_session
from broker.models import get_all_users, User
from broker.parser import user_parser


class UsersList(Resource):
    decorators = [auth.login_required]
    reqparse = user_parser

    def get(self):
        result = {user.id: user
                  for user in get_all_users()}

        return {
            "action": "get_all_users",
            "result": {
                "users": result
            }
        }

    def post(self):
        args = self.reqparse.parse_args()
        check = User.query.filter(
            User.name == args['name']
        ).first()

        if not check:
            user = User()
            for k, v in args.items():
                if v != None:
                    setattr(user, k, v)
            db_session.add(user)
            db_session.commit()

            return {
                "action": "add_user",
                "result": {
                    "id": user.id,
                    "name": user.name
                }
            }


class UserRessource(Resource):
    decorators = [auth.login_required]
    reqparse = user_parser

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
        if str(user_name) == user_name:
            args = self.reqparse.parse_args()
            user = User.query.filter(
                User.name == user_name).first()
            if user:
                changes = {}
                for k, v in args.items():
                    if v:
                        setattr(user, k, v)
                        changes[k] = v

                db_session.commit()
                return {
                    "action": "update_user",
                    "result": changes
                }

            else:
                return {
                    "action": "update_user",
                    "result": None
                }

    def delete(self, user_name):
        if str(user_name) == user_name:
            user = User.query.filter(User.name == user_name).first()
            if user:
                db_session.delete(user)
                db_session.commit()
                return {
                    "action": "del_user",
                    "result": {
                        "id": user.id,
                        "name": user.name,
                        "deleted": True
                    }
                }
            else:
                return {
                    "action": "delete_user",
                    "result": {
                        "id": None,
                        "name": user_name,
                        "deleted": False
                    }
                }
