#!/usr/bin/env python3
# coding=utf-8
from .user_model import User


def get_all_users():
    return User.query.all()


def get_all_where(field, equals, to_json=False):
    return User.query.filter(field == equals).all()


def make_members_friends(group):
    members = get_all_where(User.group, group)
    members_set = set((m for m in members))
    for member in members_set:
        work_set = members_set.difference({member})

        for new_friend in work_set:
            member.friends.append(new_friend)
            # print(work_set, new_friend, member)
    return members_set
