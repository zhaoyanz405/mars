#! /usr/bin/python

"""
@author: yan.zhao
@contact: zhaoyanz405@gmail.com
@time: 2019/11/7 16:48
"""


class HTTPError(Exception):

    def __init__(self, status_code=None, status_msg=None):
        self.status_code = status_code
        self.status_msg = status_msg


class HTTPMethodInvalidError(Exception):
    pass
