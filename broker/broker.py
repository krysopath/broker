#!/usr/bin/env python3
# coding=utf-8
from flask import Flask, jsonify, g, request, make_response
from flask_restful import Resource, Api
from interactor import Interactor, FuelModel, Fuel
from flask.ext.httpauth import HTTPBasicAuth
from fractions import Fraction as frac

app = Flask(__name__)
api = Api(app)
auth = HTTPBasicAuth()


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


class FueLRessoure(Resource):
    fuels = {
        '1': {
            'elements': {
                '_C': (500/1000),
                '_S': (2/1000),
                '_Cl': (2/1000),
                '_N': (2/1000),
                '_O': (380/1000),
                '_H': (100/1000),
                '_F': (2/1000),
                '_Ash': (12/1000)
            },
            'name': 'testfuel'
        }
    }

    @auth.login_required
    def get(self, fuel_id):
        return jsonify({fuel_id: self.fuels[fuel_id]})

    @auth.login_required
    def put(self, fuel_id):
        self.fuels[fuel_id] = request.form['data']
        return jsonify({fuel_id: self.fuels[fuel_id]})

api.add_resource(FueLRessoure, '/fuel/<string:fuel_id>')

if __name__ == '__main__':
    app.run(debug=False, port=4444, host='0.0.0.0')