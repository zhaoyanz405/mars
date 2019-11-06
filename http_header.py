#! /usr/bin/python

"""
@author: yan.zhao
@contact: zhaoyanz405@gmail.com
@time: 2019/11/6 14:57
"""


class HTTPHeader:

    def __init__(self, **kwargs):
        self._header = kwargs

    def update(self, kwargs: dict):
        self._header.update(kwargs)

    def __str__(self):
        pairs = list()
        for k, v in self._header.items():
            pairs.append("%s: %s" % (k, v))
        return "\r\n".join(pairs)


