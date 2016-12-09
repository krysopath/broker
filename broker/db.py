#!/usr/bin/env python3
# coding=utf-8
from os import mkdir, environ
from os.path import exists
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Sequence, Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import sessionmaker

__home__ = '{}//'.format(environ['HOME'])
__dbfile__ = __home__ + 'broker.db'
__dbconn__ = 'sqlite:///{}'.format(__dbfile__)

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(50))
    fullname = Column(String(100), nullable=True)
    pw_hash = Column(String(512))
    since = Column(DateTime)

    def __repr__(self):
        return "<User(name='%s', fullname='%s', pw_hash='%s')>" \
               % (self.name, self.fullname, self.pw_hash)


class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, Sequence('task_id_seq'), primary_key=True)
    name = Column(String(50))
    descript = Column(String(2048))
    done = Column(Boolean)
    since = Column(DateTime)
    by = Column(Integer)

    def __repr__(self):
        return "<Task(name='%s', descript='%s', done='%s')>" \
               % (self.name, self.descript, self.done)


engine = create_engine(__dbconn__, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

if not exists(__dbfile__):
    Base.metadata.create_all(engine)


#ed_user = User(name='ed', fullname='Ed Jones', pw_hash='234234234')
#session.add(ed_user)
#our_user = session.query(User).filter_by(name='ed').first()
#print(ed_user is our_user, our_user.pw_hash)
