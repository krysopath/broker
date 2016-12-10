#!/usr/bin/env python3
# coding=utf-8
from .user_model import User


def get_all_users():
    return User.query.all()


def get_all_where(field, equals, to_json=False):
    return User.query.filter(field == equals).all()


def make_members_friends(groupname):
    """
    for each member of groupname, add other members to member.friends

    :param groupname: a groupname of the User table
    :return a list of the modified members of given groupname
    """
    members = get_all_where(User.group, groupname)
    print(members)
    members_set = set((m for m in members))
    for member in members_set:
        work_set = members_set.difference({member})
        print('adding', work_set, 'as friends for', member)
        for new_friend in work_set:
            member.friends.append(new_friend)

    return members
