#!/usr/bin/env python3
# coding=utf-8
import time
from functools import wraps
from pprint import pprint

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class ApiError(Exception):
    pass

__uri_public__ = 'https://g:g25v09e85@endtropie.mooo.com/api/v1/users'
__uri_dev__ = 'http://g:g25v09e85@localhost:4444/api/v1/users'
__uri__ = __uri_dev__


def requester(fn):
    @wraps(fn)
    def req(*args, **kwargs):

        t = time.time()
        resp = fn(*args, **kwargs)
        tdelta = time.time() - t
        print('requested', resp.url)
        with open('last-response.txt', 'w') as last:
            last.write(resp.text)

        print(round(tdelta, 5), 'sec for', resp.request)
        if resp.status_code != 200:
            raise ApiError('{} {}'.format(resp.request, resp.url), resp.status_code)
        else:
            return resp

    return req


def decoder(fn):
    @wraps(fn)
    def req(*args, **kwargs):
        def timed():
            t = time.time()
            response = fn(*args, **kwargs)
            dtime = time.time() - t
            print(
                round(dtime, 5),
                'sec for decoding JSON'
            )
            return response, dtime

        response, dtime = timed()

        try:
            json_data = response.json()
            return json_data, response.status_code
        except TypeError:
            return "", 404
    return req


class Actor:
    verify = False

    @decoder
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
    a = Actor()
    data, status = a.request_all()
    pprint(data, )


if __name__ == "__main__":
    main()

