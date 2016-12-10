#!/usr/bin/env python3
# coding=utf-8
from .app import app
from .jsonize import jsonize
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


db = SQLAlchemy(app)

friends = db.Table(
    'friends',
    db.Column(
        'user_id', db.Integer, db.ForeignKey('user.id')
    ),
    db.Column(
        'friend_id', db.Integer, db.ForeignKey('user.id')
    ),
    db.Column(
        'creation_time', db.TIMESTAMP,
        server_default=db.func.current_timestamp(),
        nullable=False
    ),
)


class User(db.Model):
    id = db.Column(db.Integer, db.Sequence('user_id_seq'), primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    fullname = db.Column(db.String(100), nullable=True)
    group = db.Column(db.String(100), nullable=False)
    rank = db.Column(db.Integer)
    hash = db.Column(db.String(512))
    creation_time = db.Column(
        db.TIMESTAMP, server_default=db.func.current_timestamp(),
        nullable=False
    )
    friends = db.relationship(
        'User',  # defining the relationship, User is left side entity
        secondary=friends,
        primaryjoin=(friends.c.user_id == id),
        secondaryjoin=(friends.c.friend_id == id),
        lazy='dynamic'
    )

    def __repr__(self):
        return "<User(id='%s', name='%s')>" \
               % (self.id, self.name)

    def __iter__(self):
        for p in ['id', 'name', 'fullname', 'group', 'rank', 'creation_time', 'emails', 'xmpp']:
            yield p, getattr(self, p)

    def toJSON(self):
        return {pk: pv for pk, pv in self}


class Email(db.Model):
    id = db.Column(db.Integer, db.Sequence('emails_id_seq'), primary_key=True)
    addr = db.Column(db.String(150), unique=True, nullable=False)
    user_id = db.Column(db.Integer, ForeignKey('user.id'))

    user = relationship("User", back_populates="emails")

    def __repr__(self):
        return "<Email(id='%s', addr='%s')>" \
               % (self.id, self.addr)

    def __iter__(self):
        for p in ['id', 'addr']:
            yield p, getattr(self, p)

    def toJSON(self):
        return {pk: pv for pk, pv in self}


User.emails = relationship(
    "Email",
    order_by=Email.id,
    back_populates="user")


class Xmpp(db.Model):
    id = db.Column(db.Integer, db.Sequence('xmpp_id_seq'), primary_key=True)
    jid = db.Column(db.String(150), unique=True, nullable=False)
    user_id = db.Column(db.Integer, ForeignKey('user.id'))

    user = relationship("User", back_populates="xmpp")

    def __repr__(self):
        return "<XMPP(id='%s', jid='%s')>" \
               % (self.id, self.jid)

    def __iter__(self):
        for p in ['id', 'jid']:
            yield p, getattr(self, p)

    def toJSON(self):
        return {pk: pv for pk, pv in self}

User.xmpp = relationship(
    "Xmpp",
    order_by=Xmpp.id,
    back_populates="user")


def getuser():
    return db.session.query(User).first()

