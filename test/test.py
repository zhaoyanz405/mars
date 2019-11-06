#! /usr/bin/python

"""
@author: yan.zhao
@contact: zhaoyanz405@gmail.com
@time: 2019/11/6 16:34
"""
import unittest


class TestHttpHeader(unittest.TestCase):
    def test_header(self):
        from http_header import HTTPHeader
        header = HTTPHeader(server='nginx')
        self.assertIsNotNone(header._header)

        header.update({"Content-Type": "text/plain;charset=UTF-8"})
        self.assertEqual(len(header._header), 2)

        print(str(header))


if __name__ == '__main__':
    unittest.main()
