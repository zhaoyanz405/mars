#! /usr/bin/python

"""
@author: yan.zhao
@contact: zhaoyanz405@gmail.com
@time: 2019/11/6 14:12
"""
import datetime
import socket
import traceback

from exception import HTTPMethodInvalidError
from http import HTTPRequest, HTTPHeader, HTTPResponse


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

    def run(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen()
        print('server has been started. ')
        conn, addr = self.socket.accept()
        print('listening at %s' % str(addr))

        tag = "\r\n\r\n"
        msg = ""
        over_msg = ""
        while True:
            try:
                if over_msg and not msg:
                    msg = over_msg

                _msg = conn.recv(1024)
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
                        else:
                            _end = loc + len(tag)
                        msg = msg[:_end]
                    except (ValueError, HTTPMethodInvalidError):
                        print(traceback.format_exc())
                        raise
                    print('msg:', msg)
                    adapt(conn, request)
            except KeyboardInterrupt:
                break
        self.stop()

    def stop(self):
        self.socket.close()


def adapt(conn, request):
    """

    :param conn:
    :param request:
    :return:
    """

    print('------%s--------' % request.method)
    parse_query_params(request)
    if request.method == 'GET':
        response = HTTPResponse(status_code=200, status_msg='OK')
        response.content = "<h1>testst</h1>"
        response.header = HTTPHeader({
            'Date': datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT"),
            'Server': 'mars',
            'Content-Type': 'text/html',
            'Content-Length': len(response.content)
        })

        conn.send(str(response).encode('utf-8'))

    if request.method == 'POST':
        response = HTTPResponse(status_code=200, status_msg='OK')
        conn.send(str(response.response_line).encode('utf-8'))
        print(request.header)
        data = conn.recv(int(request.header['Content-Length']))
        print(data)


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


if __name__ == '__main__':
    HTTPServer(host='127.0.0.1', port=8085).run()
