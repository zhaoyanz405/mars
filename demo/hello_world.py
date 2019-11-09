#! /usr/bin/python

"""
@author: yan.zhao
@contact: zhaoyanz405@gmail.com
@time: 2019/11/9 10:41
"""
import datetime

from base import HTTPResponse, HTTPHeader
from http_server import HTTPServer
from web import RequestHandler


class Hello(RequestHandler):

    def get(self):
        res = HTTPResponse(status_code=200, status_msg='OK')
        res.content = "<h1>Hello World!</h1>"
        res.header = HTTPHeader({
            'Date': datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT"),
            'Server': 'mars',
            'Content-Type': 'text/html',
            'Content-Length': len(res.content)
        })
        self.write(res)


if __name__ == '__main__':
    server = HTTPServer(host='127.0.0.1', port=8085)
    server.register_handler({'/hello': Hello})
    server.run()
