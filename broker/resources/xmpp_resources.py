#!/usr/bin/env python3
# coding=utf-8
from flask import g
from flask_restful import Resource

from broker import auth
from broker.models import User
from broker.parser import xmpp_parser
from broker.xmpp import SendMsgBot


class SendMessage(Resource):
    decorators = [auth.login_required]
    parser = xmpp_parser

    def post(self, user_name):
        args = self.parser.parse_args()
        _from = g.user.jids[0]
        _to = User.query.filter(User.name == user_name).first().jids[0]
        _message = args['msg']

        if args:
            bot = SendMsgBot(
                _from.jid,
                "g25v09e85",
                _to,
                _message
            )
            if bot.connect():
                bot.process(block=False)
                return {
                    'result': args
                }
        return {
            'result': None
        }

    def get(self):
        args = self.parser.parse_args()
        return {
            'result': None
        }
