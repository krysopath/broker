#!/usr/bin/env python3
# coding=utf-8
from os import environ

__home__ = '{}//'.format(environ['HOME'])
__pwd__ = '{}//'.format(environ['PWD'])
__dbfile__ = 'broker.db'
__dbconn__ = 'sqlite:///{}'.format(__dbfile__)