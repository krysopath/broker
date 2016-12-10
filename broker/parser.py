#!/usr/bin/env python3
# coding=utf-8
from flask_restful import reqparse

user_parser = reqparse.RequestParser()
user_parser.add_argument('name', type=str)
user_parser.add_argument('email', type=str)
user_parser.add_argument('fullname', type=str)
user_parser.add_argument('group', type=str)
user_parser.add_argument('rank', type=int)
