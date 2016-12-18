#!/usr/bin/env python3
# coding=utf-8
from sqlalchemy import Column, Integer, Sequence, String, Table, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func

from broker.database import Base
from broker.models import User

tagstoposts = Table(
    'tags_posts',
    Base.metadata,
    Column(
        'tag_id', Integer, ForeignKey('tags.id')
    ),
    Column(
        'post_id', Integer, ForeignKey('posts.id')
    )
)


# class Post(Base):
#     __tablename__ = "posts"
#     id = Column(Integer, Sequence('posts_id_seq'), primary_key=True)


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, Sequence('posts_id_seq'), primary_key=True)
    content = Column(String(4096), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    creation_time = Column(
        TIMESTAMP,
        server_default=func.now(),
        nullable=False
    )

    user = relationship(
        "User", back_populates="posts")

    tags = relationship(
        'Tag',
        secondary=tagstoposts,
        backref=backref(
            'posts',
            lazy='dynamic'
        )
    )

    def __init__(self, content=None):
        self.content = content

    def __repr__(self):
        return "<Post(id='%s', creation_time='%s')>" \
               % (self.id, self.creation_time)


User.posts = relationship(
    "Post",
    order_by=Post.id,
    back_populates="user")


class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return "<Tag(id='%s', name='%s')>" \
               % (self.id, self.name)
