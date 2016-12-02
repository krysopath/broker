#!/usr/bin/env python3
# coding=utf-8
from flask import Flask, jsonify, g
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
    data = {'_id': "1", 'data': 'hello World!'}
    #@app.cli.command('get_interactor')
    def get(self, _id=None):
        return jsonify(self.data[_id])

api.add_resource(FueLRessoure, '/fuel/<int:_id>')

if __name__ == '__main__':
    app.run(debug=True, port=4444, host='0.0.0.0')