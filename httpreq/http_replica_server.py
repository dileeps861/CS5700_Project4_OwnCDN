import socketserver
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Tuple

from httpreq.cache_origin_http import WebDownloader
from httpreq.constants import Constants


# Internal server to handle http requests and resolve cdn
class Server(object):
    def __init__(self, port: int = Constants.REPLICA_PORT, origin: str = Constants.ORIGIN_URL):
        self.origin = origin
        self.port = port

    def start_server(self):
        # Start the server
        _server = HTTPServer(('', self.port), InternalServer)
        InternalServer.origin = self.origin
        InternalServer.port = self.port
        return _server


# Internal server to handle http requests and resolve cdn requests
# This is the server that will be used to handle the requests from the client
class InternalServer(BaseHTTPRequestHandler):
    origin = ""
    port = 8080
    web_downloader = WebDownloader()

    def __init__(self, request_: bytes, client_address: Tuple[str, int], server: socketserver.BaseServer):
        super().__init__(request_, client_address, server)

    # Overridden the do_GET method to handle the request in CDN. This method is called when a GET request is received.
    # Then it checks if the request is for grading/beacon or for a web page. If it is for a web page, it checks if the
    # page is cached. If it is cached, it returns the cached page. If it is not cached, it fetches the page from the
    # origin server and caches it. If the request is for grading/beacon, it returns the grading beacon.
    def do_GET(self):
        complete_url = Constants.HTTP_EXTENSION_CODE + self.origin + ":" + str(Constants.ORIGIN_SERVER_PORT) + \
                       self.path
        if Constants.GRADING_BEACON_URL in self.path:
            self.send_response(Constants.GRADING_BEACON_RESPONSE_CODE, "OK")
            self.send_header("Content-type", "text/html")
            self.end_headers()
            return

        response = self.web_downloader.download_website_data(complete_url, self.path)

        # Send not found response if the website was not valid.
        if response is None:
            self.send_response(Constants.HTTP_NOT_FOUND_RESPONSE_CODE, "Not Found")
            self.send_header("Content-type", "text/html")
            self.end_headers()
            return

        # Prepare the response to send back to the client.
        self.send_response(response.get_status_code())
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Length", str(len(response.get_data())))
        if response.get_headers():
            for header in response.get_headers():
                self.send_header(header, response.get_headers()[header])
        self.end_headers()
        if response.get_data():
            self.wfile.write(response.get_data())
        self.wfile.flush()


if __name__ == '__main__':
    serve = Server(7566, "cs5700cdnorigin.ccs.neu.edu")
    serv = serve.start_server()
    serv.serve_forever()
