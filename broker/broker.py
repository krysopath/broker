#!/usr/bin/env python3
# coding=utf-8
from flask import Flask, jsonify, g
from flask_restful import Resource, Api
from interactor import Interactor, FuelModel, Fuel

app = Flask(__name__)
api = Api(app)


def get_interactor():
    iactor = getattr(g, 'iactor', None)
    if iactor is None:
        iactor = g._database = Interactor('fuel', FuelModel, Fuel)
    return iactor

@app.teardown_appcontext
def teardown_db(exception):
    iactor = getattr(g, 'iactor', None)
    if iactor is not None:
        iactor.close()


class FueLRessoure(Resource):
    @app.cli.command('get_interactor')
    def get(self):
        return jsonify(g.iactor.get_data(1))

api.add_resource(FueLRessoure, '/fuel=<int:_id>')

if __name__ == '__main__':
    app.run(debug=True, port=4444, host='0.0.0.0')