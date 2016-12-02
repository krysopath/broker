#!/usr/bin/env python3
# coding=utf-8
from flask import Flask
from flask_restful import Resource, Api
from interactor import Interactor, FuelModel, Fuel

app = Flask(__name__)
api = Api(app)
i = Interactor('fuel', FuelModel, Fuel)


class FueLRessoure(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(FueLRessoure, '/')

if __name__ == '__main__':
    app.run(debug=True, port=4444, host='0.0.0.0')