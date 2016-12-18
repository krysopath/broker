#!/usr/bin/env python3
# coding=utf-8
from flask_restful import Resource

from broker import auth
from broker.parser import xmpp_parser


class SendMessage(Resource):
    decorators = [auth.login_required]
    parser = xmpp_parser

    def post(self):
        args = self.parser.parse_args()
        return args
