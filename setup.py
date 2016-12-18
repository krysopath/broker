#!/usr/bin/env python3
# coding=utf-8
from setuptools import setup

out = setup(
    name='broker',
    version='0.2',
    description='json api, with users, post, friends, messages',
    url='ssh://git@endtropie.mooo.com:22222/home/git/broker.git',
    author='Georg',
    author_email='krysopath@gmail.com',
    license='GPL',
    # packages=[
    #    'models',
    #    'ressources'
    # ],
    scripts=[
        'broker_server.py',
    ],
    install_requires=[
        'sqlalchemy',
        'flask',
        'flask_restful',
        'flask_httpauth'
    ],
    zip_safe=False
)
