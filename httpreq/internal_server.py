
# Insernal server to handle http requests and resolve dns
from http.server import HTTPServer

from tornado.web import RequestHandler


class InternalServer(object):
    def __init__(self, port=80, host=''):
        self.host = host
        self.port = port
        self.server = HTTPServer((self.host, self.port), RequestHandler)

    def start(self):
        self.server.start()
        