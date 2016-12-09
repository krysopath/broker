#!/usr/bin/env python3
# coding=utf-8
from app import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)


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

