#!/usr/bin/env python3
# coding=utf-8
import code

from broker import app
from broker.database import init_db
from broker.models import User, Post

init_db()

app.config['SECRET_KEY'] = b"something"
admins = User.query.filter(User.role == "admin").all()
users = User.query.filter(User.role == "user").all()
posts = Post.query.all()


def console():
    vars = globals().copy()
    vars.update(locals())
    shell = code.InteractiveConsole(vars)
    shell.interact()


try:
    console()
except SyntaxError:
    console()
