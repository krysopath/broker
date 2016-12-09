#!/usr/bin/env python3
# coding=utf-8
from config import __dbconn__
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = __dbconn__
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False