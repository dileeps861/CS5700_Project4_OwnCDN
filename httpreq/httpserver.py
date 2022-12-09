# This class will download the website data from the internet.

# This class will download the website data from the internet.
import os
from http.server import BaseHTTPRequestHandler
from socketserver import BaseServer
from urllib.request import Request, urlopen

from httpreq.caching import Cache
from utils.file_utils import FileUtil


class WebDownloader():
    def __init__(self, urls):

        self.url = urls
        self.headers_dict = {'Accept-Language': 'en-IN,en-US;q=0.9,en;q=0.8,hi-IN;q=0.7,hi;q=0.6,en-GB;q=0.5',
                             'Accept-Encoding': "utf-8",
                             'accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9, image / avif, '
                                       'image / webp, image / apng, * / *;q = 0.8, application / signed - exchange;v = b3;q '
                                       '= 0.9',
                             'Connection': 'keep-alive'}

    # def __init__(self, request: bytes, client_address: tuple[str, int], server: BaseServer):
    #     super().__init__(request, client_address, server)
    #     self.url = "https"
    #     self.headers_dict = {'Accept-Language': 'en-IN,en-US;q=0.9,en;q=0.8,hi-IN;q=0.7,hi;q=0.6,en-GB;q=0.5',
    #                     'Accept-Encoding': "utf-8",
    #                     'accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9, image / avif, '
    #                               'image / webp, image / apng, * / *;q = 0.8, application / signed - exchange;v = b3;q '
    #                               '= 0.9',
    #                     'Connection': 'keep-alive'}

    # Download the website data from the internet.
    def download_website_data(self):
        try:
            req = Request(self.url, headers=self.headers_dict)
            response = urlopen(req)
            return response.read()
        except Exception as e:
            print(e)
            return None

    # Override the doGet method to return a response object from DNS server if available otherwise
    # from the original requested website
    def do_GET(self):
        if self.path == "/":
            return self.download_website_data()


if __name__ == '__main__':
    # Download the website data from the internet.
    url = "https://david.choffnes.com/classes/cs5700f22/project4.php"
    web_downloader = WebDownloader(url)
    downloaded_data = web_downloader.download_website_data()
    file_parts = url.split("/")
    path = 'websites/'
    is_exist = os.path.exists(path)
    if not is_exist:
        # Create a new directory if it does not exist
        os.makedirs(path)
    file_name = str.join('_', file_parts)
    complete_name = os.path.join(path, file_name)
    FileUtil.save_website_data_in_disk(complete_name, downloaded_data)
    cache = Cache()
    cache.cache_website(url, file_name)
    print(cache.get_all_pages())
