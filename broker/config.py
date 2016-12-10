#!/usr/bin/env python3
# coding=utf-8
from os import environ

__home__ = '{}//'.format(environ['HOME'])
__dbfile__ = __home__ + 'broker.db'
__dbconn__ = 'sqlite:///{}'.format(__dbfile__)
