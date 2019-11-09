#! /usr/bin/python

"""
@author: yan.zhao
@contact: zhaoyanz405@gmail.com
@time: 2019/11/6 14:12
"""
import json
import socket
import traceback
from json import JSONDecodeError

from exception import HTTPMethodInvalidError
from base import HTTPRequest, HTTPHeader, HTTPResponse


def parse(msg):
    """解析请求头及header

    :return:
    """

    request = HTTPRequest()
    header = HTTPHeader()
    if isinstance(msg, bytes):
        msg = msg.decode('utf-8')
    print('msg', msg.split("\r\n"))
    for i, line in enumerate(msg.split("\r\n")):
        if i == 0:
            request.method, request.url, request.version = line.split(' ')
            print(line)

        if line.count(':') > 1:
            continue

        parts = line.split(':')
        if len(parts) == 2:
            header[parts[0]] = parts[1]

    request.header = header
    print('header', header)
    return request


class HTTPServer:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn = None
        self.handler_map = {}

    def register_handler(self, maps: dict):
        self.handler_map.update(maps)

    def run(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen(128)
        print('server has been started. ')
        self.conn, addr = self.socket.accept()
        print('listening at %s' % str(addr))

        tag = "\r\n\r\n"
        msg = ""
        over_msg = ""
        while True:
            try:
                if over_msg and not msg:
                    msg = over_msg

                _msg = self.conn.recv(1024)
                if not _msg:
                    print('no msg.')
                    break

                print('_msg: ', _msg)
                msg += _msg.decode('utf-8')
                loc = msg.find(tag)
                if loc:
                    # receive header end
                    over_msg = msg[loc + len(tag):]

                    try:
                        request = parse(msg)
                        content_length = request.header.get('Content-Length')
                        if content_length:
                            _end = loc + len(tag) + int(content_length)
                            request.body = msg[loc + len(tag): loc + len(tag) + int(content_length)]
                        else:
                            _end = loc + len(tag)
                        msg = msg[:_end]
                    except (ValueError, HTTPMethodInvalidError):
                        print(traceback.format_exc())
                        raise
                    print('msg:', msg)
                    self.adapt(request)
            except KeyboardInterrupt:
                break
        self.stop()

    def adapt(self, request):
        """

        :param request:
        :return:
        """
        parse_query_params(request)
        parse_body_params(request)
        cls = self.handler_map.get(request.url)
        if not cls:
            response = HTTPResponse(status_code=404, status_msg='Not Found')
            self.conn.send(str(response).encode('utf-8'))
            return

        try:
            eval('cls(request, self.conn).%s()' % request.method.lower())
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            response = HTTPResponse(status_code=500, status_msg='Server Error')
            self.conn.send(str(response).encode('utf-8'))

    def stop(self):
        self.socket.close()


def parse_query_params(request: HTTPRequest):
    """
    解析request中的query参数
    :param request:
    :return:
    """

    parts = request.url.split('?')
    if len(parts) == 2:
        request.url = parts[0]
        if '&' not in parts[1]:
            return

        for pairs in parts[1].split('&'):
            k, v = pairs.split('=')
            request.params[k] = v

    print('params:', request.params)


def parse_body_params(request: HTTPRequest):
    """
    解析request中的body参数
    :param request:
    :return:
    """
    print('body', type(request.body), request.body)
    content_type = request.header.get('Content-Type')
    if content_type and content_type.find("json") >= 0:
        try:
            request.params.update(json.loads(request.body))
        except JSONDecodeError:
            print('json format error. body: %s' % request.body)


if __name__ == '__main__':
    HTTPServer(host='127.0.0.1', port=8085).run()
