#!/usr/bin/env python3
# coding=utf-8
from flask_restful import Resource

from broker.models import get_all_users
from broker.util import requires_auth



class UsersAPI(Resource):

    @requires_auth
    def get(self):
        def results():
            result = {}
            for user in get_all_users():
                result[user.id] = user
                # print(user.id)

            resp = {"users": result}
            print(resp)
            _serialised = {
                "action": "get_all_users",
                "result": resp}

            return _serialised

        out = results()
        print(out)
        return out


# class UsersAPI(Resource):
#     @requires_auth
#     def get(self):
#         users = db.session.query(User).order_by(User.id).all()
#         results = {}
#
#         for user in users:
#             results[user.id] = dict(user)
#
#         return jsonify(results)
#
#     @requires_auth
#     def post(self):
#         args = user_parser.parse_args()
#         check = db.session.query(User).filter(
#             User.name == args['name']).first()
#         if not check:
#             user = User()
#             user.name = args['name']
#             user.group = args['group']
#             user.fullname = args['fullname'] or None
#             user.rank = args['rank'] or 100
#
#             db.session.add(user)
#             db.session.commit()
#
#             return jsonify(dict(user))
#
#         else:
#             raise UserAlreadyExistsError
#
#
# class UserAPI(Resource):
#     @requires_auth
#     def get(self, user_name):
#         user = db.session.query(User) \
#             .filter(User.name == user_name) \
#             .first()
#         if user:
#             results = {'data': dict(user)}
#             return jsonify(results)
#
#     @requires_auth
#     def put(self, user_name):
#         if not str(user_name) == user_name:
#             raise MalformedPost
#         args = user_parser.parse_args()
#         user = db.session.query(User).filter(
#             User.name == user_name).first()
#         if user:
#             changes = {}
#             for k, v in args.items():
#                 if v:
#                     setattr(user, k, v)
#                     changes[k] = v
#
#             db.session.commit()
#             return jsonify({'changes': changes})
#         else:
#             return jsonify({'changes': None})
#
#     @requires_auth
#     def delete(self, user_name):
#         if not str(user_name) == user_name:
#             raise MalformedPost
#         user = db.session.query(User).filter(
#             User.name == user_name).first()
#         if user:
#             db.session.delete(user)
#             db.session.commit()
#             return jsonify({'deleted': user_name})
#         else:
#             return jsonify({'deleted': None})
#
