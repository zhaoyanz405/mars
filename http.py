#! /usr/bin/python

"""
@author: yan.zhao
@contact: zhaoyanz405@gmail.com
@time: 2019/11/7 17:06
"""
from exception import HTTPMethodInvalidError


class HTTPHeader(dict):

    def __str__(self):
        pairs = list()
        for k, v in self.items():
            pairs.append("%s: %s" % (k, v))
        return "\r\n".join(pairs)


class HTTPRequest:
    _method = ["GET", "POST", "HEAD", "OPTION"]

    def __init__(self, method=None, url=None, version=None, header=None, **kwargs):
        if method not in self._method:
            raise HTTPMethodInvalidError

        self.method = method
        self.url = url
        self.version = version
        self.header = header  # type:HTTPHeader
        self.params = kwargs
