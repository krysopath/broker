#!/usr/bin/env python3
# coding=utf-8
from broker import app

if __name__ == '__main__':
    context = ('../certs/broker.crt',
               '../certs/broker.key')
    app.run(
        host='0.0.0.0',
        port=4444,
        # ssl_context=context,
        threaded=True,
        debug=True)
