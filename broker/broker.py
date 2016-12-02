#!/usr/bin/env python3
# coding=utf-8
from flask import Flask, jsonify, g, request
from flask_restful import Resource, Api
from interactor import Interactor, FuelModel, Fuel

app = Flask(__name__)
api = Api(app)


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
    fuels = {'1': {'data': 'blabla'}}
    def get(self, fuel_id):
        return jsonify({fuel_id: self.fuels[fuel_id]})

    def put(self, fuel_id):
        self.fuels[fuel_id] = request.form['data']
        return jsonify({fuel_id: self.fuels[fuel_id]})

api.add_resource(FueLRessoure, '/fuel/<string:fuel_id>')

if __name__ == '__main__':
    app.run(debug=True, port=4444, host='0.0.0.0')