#!/usr/bin/env python3
# coding=utf-8
from sqlalchemy import Column, Integer, Sequence, String, Table, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from broker.database import Base

friends = Table(
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
    hash = Column(String(512))
    creation_time = Column(
        TIMESTAMP,
        server_default=func.now(),
        nullable=False
    )
    friends = relationship(
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


class Email(Base):
    __tablename__ = "emails"
    id = Column(Integer, Sequence('emails_id_seq'), primary_key=True)
    addr = Column(String(150), unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship(
        "User", back_populates="emails")

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


class JID(Base):
    __tablename__ = "jids"
    id = Column(Integer, Sequence('jids_id_seq'), primary_key=True)
    jid = Column(String(150), unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="jids")

    def __repr__(self):
        return "<XMPP(id='%s', jid='%s')>" \
               % (self.id, self.jid)

    def __iter__(self):
        for p in ['id', 'jid']:
            yield p, getattr(self, p)

    def toJSON(self):
        return {pk: pv for pk, pv in self}


User.jids = relationship(
    "JID",
    order_by=JID.id,
    back_populates="user")
