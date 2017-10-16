#!/usr/bin/env python3
# coding=utf-8
from flask import g
from flask_restful import Resource

from broker import auth


class GetToken(Resource):
    decorators = [auth.login_required]

    def get(self):
        token = g.user.generate_auth_token()
        return {
            "action": "get_new_token",
            "result": {
                "token": token.decode('utf-8')
            }
        }
