#!/usr/bin/env python3
# coding=utf-8

from datetime import datetime
from functools import wraps
from json import JSONEncoder, dumps

from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm.collections import InstrumentedList
from sqlalchemy.orm.query import Query

__date_as_string__ = False


class DataEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            fields = {}
            for field in [x for x in dir(obj)
                          if not x.startswith('_')

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
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class

            fields = {}
            for field in [x for x in dir(obj)
                          if not x.startswith('_')
                          and x not in ['metadata',
                                        'query',
                                        'query_class',
                                        'generate_auth_token',
                                        'set_hash',
                                        'check_hash',
                                        'verify_auth_token',
                                        'hash']]:
                data = obj.__getattribute__(field)
                try:
                    # print('AlchemyEncoder:', data.__class__, data)
                    dumps(data)  # this will fail on non-encodable values, like other classes
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
                                'sec': data.second, }

                    elif isinstance(data, InstrumentedList):
                        fields[field] = [
                            {'id': x.id,
                             'obj': x} for x in data]

                    elif isinstance(data, Query):
                        fields[field] = [
                            {'id': x.id,
                             'obj': x.name} for x in data.all()]

                    else:
                        fields[field] = "Unhandled: ", field, data.__str__(), obj.__str__()

                        # obj.__serialised = True

            #print("encoded to", type(fields))
            return fields


class APIEncoder(JSONEncoder):
    def default(self, obj):

        if isinstance(obj.__class__, DeclarativeMeta):
            # print("encoding",
            #      obj.__class__,
            #      "with", AlchemyEncoder)

            return AlchemyEncoder(
                indent=None,
                check_circular=False
            ).default(obj)


def jsonize(obj):
    @wraps(obj)
    def wrapped(*args,
                **kwargs):
        result = obj(*args,
                     **kwargs)
        return dumps(
            result,
            cls=APIEncoder,
            indent=None
        )
    return wrapped
