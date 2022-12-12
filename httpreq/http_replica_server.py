import socketserver
import sys
import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Tuple
from urllib.request import Request, urlopen

from httpreq.cache_origin_http import LocalResponse
from httpreq.caching import Cache
from httpreq.constants import Constants
from httpreq.sqlite_cache import CacheWithDB
from utils.file_utils import FileUtil

_origin = ""
_port = 0
_TOTAL_ALLOWED_SPACE = Constants.TOTAL_ALLOWED_SPACE
_cache = Cache(_TOTAL_ALLOWED_SPACE)


# Internal server to handle http requests and resolve cdn
class Server(object):

    def __init__(self, port: int = Constants.REPLICA_PORT, origin: str = Constants.ORIGIN_URL):
        global _origin
        global _port
        global _TOTAL_ALLOWED_SPACE
        global _cache
        _origin = origin
        _port = port
        _TOTAL_ALLOWED_SPACE = Constants.MAX_ALLOWED_SPACE - FileUtil.estimate_space()
        _cache = CacheWithDB()

    def start_server(self):
        # Start the server
        _server = ThreadingHTTPServer(('', _port), InternalServer)
        return _server


# Internal server to handle http requests and resolve cdn requests
# This is the server that will be used to handle the requests from the client
class InternalServer(BaseHTTPRequestHandler):

    def __init__(self, request_: bytes, client_address: Tuple[str, int], server: socketserver.BaseServer):
        super().__init__(request_, client_address, server)
    # Overridden the do_GET method to handle the request in CDN. This method is called when a GET request is received.
    # Then it checks if the request is for grading/beacon or for a web page. If it is for a web page, it checks if the
    # page is cached. If it is cached, it returns the cached page. If it is not cached, it fetches the page from the
    # origin server and caches it. If the request is for grading/beacon, it returns the grading beacon.
    def do_GET(self):
        complete_url = Constants.HTTP_EXTENSION_CODE + _origin + ":" + str(Constants.ORIGIN_SERVER_PORT) + \
                       self.path
        if Constants.GRADING_BEACON_URL in self.path:
            self.send_response(Constants.GRADING_BEACON_RESPONSE_CODE, "OK")
            self.send_header("Content-type", "text/html")
            self.end_headers()
            return

        response = InternalServer.download_website_data(complete_url, self.path)

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

    @staticmethod
    def download_website_data(complete_url, data_path) -> LocalResponse:
        if _cache.is_website_present_in_cache(data_path):
            return LocalResponse(_cache.get_cached_website(data_path), 200)

        # file_name = FileUtil.generate_file_name(data_path)
        # complete_file_name = FileUtil.generate_file_path(Constants.FILE_DIRECTORY, file_name)
        # if FileUtil.is_website_data_present_in_disk(complete_file_name):
        #     try:
        #         data = FileUtil.get_website_data_from_disk(complete_file_name)
        #         _cache.cache_website(data_path, data)
        #         return LocalResponse(data, 200)
        #
        #     except Exception as e:
        #         print(e)
        #
        # try:
        #     req = Request(complete_url, headers=headers_dict)
        #     response = urlopen(req)
        #     downloaded_data = response.read()
        #
        #     FileUtil.create_dir_if_not_exists(Constants.FILE_DIRECTORY)
        #
        #     # Save the website data in disk.
        #     # This is done to avoid downloading the website again and again.
        #     # Save is done in a separate thread to avoid blocking the main thread.
        #     # This is done to serve the request as soon as possible while saving the website data in disk.
        #
        #     # threading.Thread(target=FileUtil.save_website_data_in_disk, args=(complete_file_name, downloaded_data))\
        #     #     .start()
        #     # FileUtil.save_website_data_in_disk(complete_file_name, downloaded_data)
        #     was_pop, popped_path = _cache.cache_website(data_path, downloaded_data)
        #     if was_pop:
        #         file_name = FileUtil.generate_file_name(popped_path)
        #         complete_file_name = FileUtil.generate_file_path(Constants.FILE_DIRECTORY, file_name)
        #         # threading.Thread(target=FileUtil.delete_website_data_from_disk, args=complete_file_name) \
        #         #     .start()
        #
        #     return LocalResponse(downloaded_data, Constants.HTTP_STATUS_CODE_OK)
        #
        # except Exception as e:
        #     return LocalResponse("", Constants.HTTP_NOT_FOUND_RESPONSE_CODE)

        if _cache.is_website_present_in_cache(data_path):
            print("Website is present in cache")
            return LocalResponse(_cache.get_website_data(data_path), 200)
        try:
            req = Request(complete_url)
            response = urlopen(req)
            downloaded_data = response.read()
            _cache.cache_website(data_path, downloaded_data)
            return LocalResponse(downloaded_data, Constants.HTTP_STATUS_CODE_OK)

        except Exception as e:
            return LocalResponse("", Constants.HTTP_NOT_FOUND_RESPONSE_CODE)


if __name__ == '__main__':
    serve = Server(7566, "cs5700cdnorigin.ccs.neu.edu")
    serv = serve.start_server()
    thread = threading.Thread(target=serv.serve_forever)
    thread.daemon = True

    thread.start()
    try:
        while 1:
            time.sleep(1)
            sys.stderr.flush()
            sys.stdout.flush()


    except KeyboardInterrupt:
        pass
    finally:
        serv.shutdown()

    print("Starting server, use <Ctrl-C> to stop")
