# Internal server to handle http requests and resolve dns
import socketserver
import urllib.request
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Tuple
from urllib import request

from tornado.web import RequestHandler

from httpreq.constants import Constants
from httpreq.httpserver import WebDownloader


class Server(object):
    def __init__(self, port: int, origin: str):
        self.origin = origin
        self.port = port

    def start_server(self):
        # Start the server
        serve = HTTPServer(('', self.port), InternalServer)
        InternalServer.origin = self.origin
        InternalServer.port = self.port
        return serve


class InternalServer(BaseHTTPRequestHandler):
    origin = ""
    port = 8080

    def __init__(self, request_: bytes, client_address: Tuple[str, int], server: socketserver.BaseServer):
        super().__init__(request_, client_address, server)

    def do_GET(self):
        # self.client_address

        complete_url = Constants.HTTP_EXTENSION_CODE + self.origin+":"+str(Constants.ORIGIN_SERVER_PORT) +\
                       self.headers['path']
        print(complete_url)
        web_downloader = WebDownloader()
        if self.headers['path'] in Constants.ORIGIN_SERVER_PAGE_URL:
            print("Origin server page")
            self.send_response(Constants.LANDING_URL_RESPONSE_CODE, "OK")
            self.send_header("Content-type", "text/html")
            self.end_headers()
            return

        return web_downloader.download_website_data(complete_url)

if __name__ == '__main__':
    serve = Server(7566, "en.wikipedia.org")
    serv = serve.start_server()
    serv.serve_forever()
