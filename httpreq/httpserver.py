# This class will download the website data from the internet.

# This class will download the website data from the internet.
import os
from http.server import BaseHTTPRequestHandler
from socketserver import BaseServer
from urllib.request import Request, urlopen

from httpreq.caching import Cache
from utils.file_utils import FileUtil


class WebDownloader:
    def __init__(self):
        self.headers_dict = {'Accept-Language': 'en-IN,en-US;q=0.9,en;q=0.8,hi-IN;q=0.7,hi;q=0.6,en-GB;q=0.5',
                             'Accept-Encoding': "utf-8",
                             'accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9, image / avif, '
                                       'image / webp, image / apng, * / *;q = 0.8, application / signed - exchange;v = b3;q '
                                       '= 0.9',
                             'Connection': 'keep-alive'}
        self.cache = Cache()

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
    def download_website_data(self, complete_url):
        if self.cache.is_website_present_in_cache(complete_url):
            return self.cache.get_website_data(complete_url)
        try:
            req = Request(complete_url, headers=self.headers_dict)
            response = urlopen(req)
            return response.read()
        except Exception as e:
            print(e)
            return None


if __name__ == '__main__':
    # Download the website data from the internet.
    url = "https://google.com/"
    web_downloader = WebDownloader(url)
    downloaded_data = web_downloader.download_website_data()
    file_parts = url.split("/")
    path = 'websites/'
    is_exist = os.path.exists(path)
    if not is_exist:
        # Create a new directory if it does not exist
        os.makedirs(path)
    print(file_parts[-1].strip().split("."))
    if len(file_parts[-1].strip().split(".")) <= 0 or file_parts[-1].strip().split(".")[0] == "":
        file_parts.append("index.html")
    file_name = str.join('_', file_parts)
    complete_name = os.path.join(path, file_name)
    FileUtil.save_website_data_in_disk(complete_name, downloaded_data)
    print("File saved in disk")
    print(FileUtil.get_website_data_from_disk(complete_name))
    cache = Cache()
    cache.cache_website(url, file_name)
    print(cache.get_all_pages())
