#!/usr/bin/env python3
# coding=utf-8
from flask import Flask, jsonify, g, request, make_response
from flask_restful import Resource, Api, reqparse, abort
from flask_httpauth import HTTPBasicAuth

from interactor import Interactor, FuelModel, Fuel
from fractions import Fraction as frac

app = Flask(__name__)
api = Api(app)
auth = HTTPBasicAuth()
parser = reqparse.RequestParser()
parser.add_argument('fuel')
fuels = {
    '1': {
        'elements': {
            '_C': (500 / 1000),
            '_S': (2 / 1000),
            '_Cl': (2 / 1000),
            '_N': (2 / 1000),
            '_O': (380 / 1000),
            '_H': (100 / 1000),
            '_F': (2 / 1000),
            '_Ash': (12 / 1000)
        },
        'name': 'testfuel 1'
    },
    '2': {
        'elements': {
            '_C': (496 / 1000),
            '_S': (4 / 1000),
            '_Cl': (0 / 1000),
            '_N': (6 / 1000),
            '_O': (360 / 1000),
            '_H': (120 / 1000),
            '_F': (2 / 1000),
            '_Ash': (12 / 1000)
        },
        'name': 'testfuel 2'
    }
}

@auth.get_password
def get_password(username):
    if username == 'g':
        return 'g25v09e85'
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


def get_interactor():
    iactor = getattr(g, '_iactor', None)
    if iactor is None:
        iactor = g._iactor = Interactor('fuel', FuelModel, Fuel)
    return iactor


@app.teardown_appcontext
def teardown_db(exception):
    iactor = getattr(g, '_iactor', None)
    if iactor is not None:
        iactor.close()


def abort_if_id_doesnt_exist(_id):
    if _id not in fuels:
        abort(404, message="item {} doesn't exist".format(_id))


class FueLRessoure(Resource):

    @auth.login_required
    def get(self, fuel_id):
        return jsonify(
            {fuel_id: fuels[fuel_id]}
        )

    @auth.login_required
    def put(self, fuel_id):
        fuels[fuel_id] = request.form['data']
        return jsonify(
            {fuel_id: fuels[fuel_id]}
        )

    @auth.login_required
    def delete(self, _id):
        abort_if_id_doesnt_exist(_id)
        del fuels[_id]
        return '', 204


class FuelList(Resource):
    @auth.login_required
    def get(self):
        return jsonify(fuels)

    #def post(self):
    #    args = parser.parse_args()
    #    todo_id = int(max(fuels.keys()).lstrip('todo')) + 1
    #    todo_id = 'todo%i' % todo_id
    #    fuels[todo_id] = {'task': args['task']}
    #    return jsonify(fuels([todo_id])), 201

api.add_resource(FueLRessoure, '/fuel/<string:fuel_id>')
api.add_resource(FuelList, '/fuels')

if __name__ == '__main__':
    app.run(debug=True, port=4444, host='0.0.0.0')