#!/usr/bin/env python3
# coding=utf-8
from flask_restful import Resource, fields, marshal_with, reqparse

from exceptions import *

resource_fields = {
    'name': fields.String,
    'address': fields.String,
    'date_updated': fields.DateTime(dt_format='rfc822'),
}
DATA = {'todos': {}}
parser = reqparse.RequestParser()
parser.add_argument('task', type=str, help='Explanation of task')
parser.add_argument('rate', type=int, help='Rate to charge for this resource')
parser.add_argument('done', type=bool, help='Is this task done?', )


class Todo2(Resource):
    @marshal_with(resource_fields, envelope='resource')
    def get(self, **kwargs):
        return db_get_todo()  # Some function that queries the db


def abort_if_something_wrong(todo_id):
    if todo_id not in DATA['todos']:
        raise ResourceDoesNotExist


class NoCapsString(fields.Raw):
    def format(self, value):
        return value.lower()


class Todo(Resource):
    c_key = 'todos'

    def get(self, todo_id):
        abort_if_something_wrong(todo_id)
        return DATA[self.c_key][todo_id], 200

    def delete(self, todo_id):
        abort_if_something_wrong(todo_id)
        del DATA[self.c_key][todo_id]
        return '', 204

    def put(self, todo_id):
        args = parser.parse_args()
        todo = {
            'task': args['task'] or DATA[self.c_key][todo_id]['task'],
            'rate': args['rate'] or DATA[self.c_key][todo_id]['rate'],
            'done': args['done'] or DATA[self.c_key][todo_id]['done']
        }
        DATA[self.c_key][todo_id] = todo
        return todo, 201


class TodoList(Resource):
    def get(self):
        return DATA['todos']

    def post(self):
        args = parser.parse_args()
        print(args.items())

        if DATA['todos'].keys():
            todo_id = int(
                max(
                    DATA['todos'].keys()
                ).lstrip('todo')
            ) + 1
        else:
            todo_id = 1
        todo_id = 'todo%i' % todo_id

        DATA['todos'][todo_id] = {
            'task': args['task'],
            'rate': args['rate']
        }
        return DATA['todos'][todo_id], 201

