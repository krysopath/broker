#!/usr/bin/env python3
# coding=utf-8

from datetime import datetime
from functools import wraps
from json import JSONEncoder, dumps

from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm.collections import InstrumentedList
from sqlalchemy.orm.query import Query

__date_as_string__ = False


# if isinstance(data, datetime.datetime):
#     if __date_as_string__:
#         fields[field] = str(data)
#     else:
#         fields[field] = {
#             'year': data.year,
#             'month': data.month,
#             'day': data.day,
#             'hour': data.hour,
#             'min': data.minute,
#             'sec': data.second,
#         }
#
# elif isinstance(data, Query):
#     fields[field] = None  # [x for x in data.all()]
#
# elif isinstance(data, set):
#     fields[field] = None  # [x for x in data]
#
# elif isinstance(data, User):
#     fields[field] = {
#         'id': int(data.id),
#         'name': str(data.name),
#     }
# else:
#     print('found some stuff in', type(data))
#     print('unhandled:', data)
#     fields[field] = None
# elif isinstance(obj.__class__, InstrumentedList):
#
# fields[field] = [n.id for n in data]
# return


class DataEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            fields = {}
            for field in [x for x in dir(obj)
                          if not x.startswith('_')
                          # and x not in ['metadata', 'query', 'query_class']
                          ]:
                data = obj.__getattribute__(field)
                try:
                    print('in DataEnc', data)
                    dumps(data)
                    fields[field] = data
                except TypeError:
                    fields[field] = "Error while encoding"
            return fields


class AlchemyEncoder(JSONEncoder):
    def non_default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):

            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj)
                          if not x.startswith('_')
                          and x not in ['metadata', 'query', 'query_class']]:
                data = obj.__getattribute__(field)
                try:
                    #print('in AlchEnc', data, data.__class__)
                    dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    if isinstance(data, datetime):
                        if __date_as_string__:
                            fields[field] = str(data)
                        else:
                            fields[field] = {
                                'year': data.year,
                                'month': data.month,
                                'day': data.day,
                                'hour': data.hour,
                                'min': data.minute,
                                'sec': data.second,
                            }

                    elif isinstance(data, InstrumentedList):
                        fields[field] = "IntrumentedList"

                    elif isinstance(data, Query):
                        fields[field] = [x.id for x in data.all()]

                    else:
                        fields[field] = "Error"

                    obj.__serialised = True

            print("encoding", fields)
            return fields


class APIEncoder(JSONEncoder):
    def default(self, obj):
        print(obj, obj.__class__)

        if isinstance(obj.__class__, DeclarativeMeta):
            print("encoding", obj.__class__, "with", AlchemyEncoder)

            return AlchemyEncoder(indent=0, check_circular=False).non_default(obj)

        if isinstance(obj, datetime):
            print("decoding", obj.__class__, "with", DataEncoder)
            return DataEncoder(indent=2).default(obj)




def jsonifier(obj):
    @wraps(obj)
    def wrapped(*args, **kwargs):
        result = obj(*args, **kwargs)
        return dumps(result, cls=APIEncoder, indent=4)

    return wrapped
