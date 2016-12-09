#!/usr/bin/env python3
# coding=utf-8
from flask_restful import HTTPException

errors = {
    'UserAlreadyExistsError': {
        'message': "A user with that username already exists.",
        'status': 409,
    },
    'ResourceDoesNotExist': {
        'message': "A resource with that ID no longer exists.",
        'status': 410,
        'extra': "Any extra information you want.",
    },
    'UserNotAuthed': {
        'message': "The user is not authenticated",
        'status': 401,
        'extra': ".",
    },
    'NotForYourEyes': {
        'message': "You have no access on this data.",
        'status': 403,
        'extra': "This honey is not for you.",
    },
    'MalformedPost': {
        'message': "Send a malformed post request.",
        'status': 422,
        'extra': "Learn your json!",
    },
}


class ResourceDoesNotExist(HTTPException):
    code = 410


class UserAlreadyExistsError(HTTPException):
    code = 409


class UserNotAuthed(HTTPException):
    code = 401


class NotForYourEyes(HTTPException):
    code = 403


class MalformedPost(HTTPException):
    code = 422