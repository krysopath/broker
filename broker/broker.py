#!/usr/bin/env python3
# coding=utf-8
from flask import Flask, jsonify
from flask_restful import Resource, Api
from interactor import Interactor, FuelModel, Fuel

app = Flask(__name__)
api = Api(app)
i = Interactor('fuel', FuelModel, Fuel)


class FueLRessoure(Resource):
    def get(self, _id):
        return jsonify(i.get_data(_id))

api.add_resource(FueLRessoure, '/fuel=<int:_id>')

if __name__ == '__main__':
    app.run(debug=True, port=4444, host='0.0.0.0')