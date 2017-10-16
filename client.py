#!/usr/bin/env python3
# coding=utf-8
from pprint import pprint
from random import choice
from string import ascii_letters

from client_libs import Actor

__uri_public__ = 'https://{}:{}@endtropie.mooo.com/api/v2/{}'
__uri_dev__ = 'https://{}:{}@localhost:4444/api/v2/{}'
__uri__ = __uri_dev__


def main():
    a = Actor(__uri__, "krysopath", "g25v09e85")

    data, status = a.request_all()
    pprint(data['result'])
    data, status = a.add_user(**new_user)
    pprint(data['result'])
    data, status = a.get_user(new_user['name'])
    pprint(data['result'])
    data, status = a.request_all()
    pprint(data['result'])
    data, status = a.update_user(new_user['name'], group="admin")
    pprint(data['result'])
    data, status = a.request_all()
    pprint(data['result'])
    # data, status = a.del_user(new_user['name'])
    # pprint(data['result'])


new_user = {
    'name': "test-" + "".join(
        [choice(ascii_letters).upper()
         for x in range(20)]
    ),
    'fullname': "test",
    'email': "test@mail.com",
    'role': "user",
    'rank': 10
}
if __name__ == "__main__":
    main()
