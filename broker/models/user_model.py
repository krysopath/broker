#!/usr/bin/env python3
# coding=utf-8
import bcrypt
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from sqlalchemy import Column, Integer, BigInteger, Sequence, String, Table, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from broker import app
from broker.database import Base

Friends = Table(
    'friends',
    Base.metadata,
    Column(
        'user_id', Integer, ForeignKey('users.id')
    ),
    Column(
        'friend_id', Integer, ForeignKey('users.id')
    ),
    Column(
        'creation_time', TIMESTAMP,
        server_default=func.now(),
        nullable=False
    ),
)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, Sequence('users_id_seq'), primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    fullname = Column(String(100), nullable=True)
    group = Column(String(100), nullable=False)
    rank = Column(Integer)
    reputation = Column(BigInteger)
    hash = Column(String(512))
    creation_time = Column(
        TIMESTAMP,
        server_default=func.now(),
        nullable=False
    )
    friends = relationship(
        'User',  # defining the relationship, User is left side entity
        secondary=Friends,
        primaryjoin=(Friends.c.user_id == id),
        secondaryjoin=(Friends.c.friend_id == id),
        lazy='dynamic'
    )

    def __init__(self, name=None, fullname=None, group=None, rank=None):
        self.name = name
        self.fullname = fullname
        self.group = group
        self.rank = rank

    def __repr__(self):
        return "<User(id=%r, name=%r)>" \
               % (self.id, self.name,)

    def __iter__(self):
        for p in ['id',
                  'name',
                  'fullname',
                  'group',
                  'rank',
                  'creation_time',
                  'emails',
                  'jids',
                  'friends',
                  'reputation']:
            yield p, getattr(self, p)

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def set_hash(self, pw):
        if not self.hash:
            self.hash = bcrypt.hashpw(pw, bcrypt.gensalt(14))
        else:
            raise RuntimeWarning("Process tried to reset hash")

    def check_hash(self, pw):
        if bcrypt.checkpw(pw, self.hash):
            return True
        else:
            raise RuntimeWarning("User supplied password doesnt match hash")

    def generate_auth_token(self, expiration=60):
        print("making a token for", self.name)
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id, 'name': self.name})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            token_data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None

        user = User.query.get(token_data['id'])
        print("verified token of", token_data['name'])
        return user

    def __str__(self):
        return self.name


class Email(Base):
    __tablename__ = "emails"
    id = Column(Integer, Sequence('emails_id_seq'), primary_key=True)
    addr = Column(String(150), unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship(
        "User", back_populates="emails")

    def __init__(self, addr=None):
        self.addr = addr

    def __repr__(self):
        return "<Email(id='%s', addr='%s')>" \
               % (self.id, self.addr)

    def __iter__(self):
        for p in ['id', 'addr']:
            yield p, getattr(self, p)

    def __str__(self):
        return self.addr


User.emails = relationship(
    "Email",
    order_by=Email.id,
    back_populates="user")


class JID(Base):
    __tablename__ = "jids"
    id = Column(Integer, Sequence('jids_id_seq'), primary_key=True)
    jid = Column(String(150), unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="jids")

    def __init__(self, jid=None):
        self.jid = jid

    def __repr__(self):
        return "<JID(id='%s', jid='%s')>" \
               % (self.id, self.jid)

    def __iter__(self):
        for p in ['id', 'jid']:
            yield p, getattr(self, p)

    def __str__(self):
        return self.jid


User.jids = relationship(
    "JID",
    order_by=JID.id,
    back_populates="user")
