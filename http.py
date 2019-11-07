#! /usr/bin/python

"""
@author: yan.zhao
@contact: zhaoyanz405@gmail.com
@time: 2019/11/7 17:06
"""


class HTTPHeader(dict):

    def __str__(self):
        pairs = list()
        for k, v in self.items():
            pairs.append("%s: %s" % (k, v))
        return "\r\n".join(pairs)


class HTTPRequest:
    _method = ["GET", "POST", "HEAD", "OPTION"]

    def __init__(self, method=None, url=None, version=None, header=None, **kwargs):
        self.method = method
        self.url = url
        self.version = version
        self.header = header  # type:HTTPHeader
        self.params = kwargs


class HTTPResponse:

    def __init__(self, status_code: int = None, status_msg: str = None, header=None, content=None):
        self.version = "HTTP/1.1"
        self.status_code = status_code
        self.status_msg = status_msg
        self.header = header
        self.content = content

    @property
    def response_line(self):
        return "%s %s %s\r\n" % (self.version, self.status_code, self.status_msg)

    def __str__(self):
        return "%s%s\r\n\r\n%s" % (self.response_line, str(self.header), self.content)
