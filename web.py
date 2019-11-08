#! /usr/bin/python

"""
@author: yan.zhao
@contact: zhaoyanz405@gmail.com
@time: 2019/11/8 17:40
"""
from exception import HTTPError
from http import HTTPRequest


class RequestHandler:

    def __init__(self, request=None, conn=None):
        self.request = request  # type: HTTPRequest
        self.conn = conn

    def get(self): raise HTTPError(405)

    def post(self): raise HTTPError(405)

    def head(self): raise HTTPError(405)

    def put(self): raise HTTPError(405)

    def delete(self): raise HTTPError(405)

    def patch(self): raise HTTPError(405)

    def options(self): raise HTTPError(405)

    def connect(self): raise HTTPError(405)

    def trace(self): raise HTTPError(405)

    def write(self, response=None):
        self.conn.send(str(response).encode('utf-8'))
