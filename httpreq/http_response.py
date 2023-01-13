# This class will download the website data from the internet.

# This class will download the website data from the internet.
import threading
from urllib.request import Request, urlopen

from httpreq.caching import Cache
from httpreq.constants import Constants
from utils.file_utils import FileUtil


# This class represents the response of the web_downloader.
class LocalResponse:
    def __init__(self, data, status_code, headers=None):
        self.data = data
        self.status_code = status_code
        self.headers = headers

    def get_data(self):
        return self.data

    def get_status_code(self):
        return self.status_code

    def get_headers(self):
        return self.headers
