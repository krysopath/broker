#!/usr/bin/env python3
# coding=utf-8
from broker import app

if __name__ == '__main__':
    context = ('broker/certs/broker.crt',
               'broker/certs/broker.key')
    app.config['SECRET_KEY'] = "something"
    app.run(
        host='0.0.0.0',
        port=4444,
        ssl_context=context,
        threaded=True,
        debug=True
    )
