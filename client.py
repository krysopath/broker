#!/usr/bin/env python3
# coding=utf-8
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import time
from functools import wraps
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class ApiError(Exception):
    pass

__uri_public__ = 'https://g:g25v09e85@endtropie.mooo.com/api/v1/users'
__uri_dev__ = 'https://g:g25v09e85@localhost:4444/api/v1/users'
__uri__ = __uri_dev__


def requester(fn):
    @wraps(fn)
    def req(*args, **kwargs):
        t = time.time()
        resp = fn(*args, **kwargs)
        tdelta = time.time() - t
        print(round(tdelta, 5), 'seconds for', resp.request)
        if resp.status_code != 200:
            raise ApiError('{} {}'.format(resp.request, resp.url), resp.status_code)
        else:
            return resp.json()

    return req


class Actor:
    verify = False

    @requester
    def request_all(self):
        return requests.get(
            __uri__,
            verify=self.verify
        )

    @requester
    def get_user(self, name):
        return requests.get(
            __uri__ + "/%s" % name,
            verify=self.verify
        )

    @requester
    def update_user(self,
                    username,
                    **user_args):
        return requests.put(
            __uri__ + "/%s" % username,
            json=user_args,
            verify=self.verify
        )

    @requester
    def add_user(self, **user_args):
        return requests.post(
            __uri__,
            json=user_args,
            verify=self.verify
        )

    @requester
    def del_user(self, name):
        return requests.delete(
            __uri__ + "/%s" % name,
            verify=self.verify
        )

    @requester
    def get_adresses(self, name):
        return requests.get(
            __uri__ + "/%s" % name, verify=self.verify
        )


def main():
    for n in range(100):
        a.add_user(**{'group': 'admin', 'fullname': 'piedro', 'name': 'piedro-%s' % n, 'rank': -1})
    users = a.request_all()
    for u in users:
        print(u, users[u])


a = Actor()
if __name__ == "__main__":
    main()

