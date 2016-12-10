#!/usr/bin/env python3
# coding=utf-8
import datetime
from json import JSONEncoder, dumps

from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm.collections import InstrumentedList, InstrumentedSet, InstrumentedDict
from sqlalchemy.orm.query import Query

__date_as_string__ = False


class ComplexEncoder(JSONEncoder):
    def default(self, obj):
        def make(thing2json):

            if hasattr(thing2json, 'toJSON'):
                return JSONEncoder.default(self, thing2json.toJSON())
            else:
                try:
                    return JSONEncoder.default(self, thing2json)
                except TypeError as te:
                    return "Error while serialising"

        if isinstance(obj, InstrumentedList):
            print(obj, type(obj))
            result = []
            for ele in obj:
                result.append(
                    make(ele)
                )
        elif isinstance(obj, InstrumentedSet):
            print(obj, type(obj))
            result = {make(ele) for ele in obj}

        elif isinstance(obj, InstrumentedDict):
            print(obj, type(obj))
            result = {make(k): make(v) for k, v in obj.items()}

        else:
            print(obj, type(obj))
            result = make(obj)

        return result


class AlchemyEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj)
                          if not x.startswith('_')
                          and x not in ['metadata', 'query', 'query_class', 'toJSON']]:
                data = obj.__getattribute__(field)
                try:
                    dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    if isinstance(data, datetime.datetime):
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
                                'microsec': data.microsecond
                            }
                    elif isinstance(data, InstrumentedList):
                        fields[field] = [dict(n) for n in data]
                    elif isinstance(data, Query):
                        fields[field] = [
                            {'id': n.id,
                             'name': n.name,
                             'rank': n.rank,
                             } for n in data.all()
                            ]

                    elif isinstance(data, set):
                        fields[field] = [x for x in data]
                    else:
                        print('found some stuff in', type(data))
                        print('unhandled:', data)
                        fields[field] = None

            # a json-encodable dict
            return fields
        try:
            return JSONEncoder.default(self, obj)
        except TypeError as te:

            raise te


def jsonize(obj, indent=2):
    return dumps(obj, cls=AlchemyEncoder, indent=indent)



