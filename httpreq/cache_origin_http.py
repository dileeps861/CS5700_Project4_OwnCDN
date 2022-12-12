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


# This class will download the website data from the internet.
# First it checks if the website is cached. If it is cached, it returns the cached data.
# If it is not cached, it fetches the website from the internet and caches it.
class WebDownloader:
    def __init__(self):
        self.headers_dict = {'Accept-Language': 'en-IN,en-US;q=0.9,en;q=0.8,hi-IN;q=0.7,hi;q=0.6,en-GB;q=0.5',
                             'Accept-Encoding': "utf-8",
                             'accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9, image / '
                                       'avif, '
                                       'image / webp, image / apng, * / *;q = 0.8, application / signed - exchange;v '
                                       '= b3;q '
                                       '= 0.9',
                             'Connection': 'keep-alive'}
        self.cache = Cache()

    # Download the website data from the internet.
    def download_website_data(self, complete_url, data_path) -> LocalResponse:
        if self.cache.is_website_present_in_cache(data_path):
            try:
                downloaded_data = FileUtil.get_website_data_from_disk(FileUtil.generate_file_name(data_path))
                return LocalResponse(downloaded_data, 200)
            except Exception as e:
                print(e)
        try:
            req = Request(complete_url, headers=self.headers_dict)
            response = urlopen(req)
            downloaded_data = response.read()
            file_name = FileUtil.generate_file_name(data_path)
            complete_file_name = FileUtil.generate_file_path(Constants.FILE_DIRECTORY, file_name)
            FileUtil.create_dir_if_not_exists(Constants.FILE_DIRECTORY)

            # Save the website data in disk.
            # This is done to avoid downloading the website again and again.
            # Save is done in a separate thread to avoid blocking the main thread.
            # This is done to serve the request as soon as possible while saving the website data in disk.

            # threading.Thread(target=FileUtil.save_website_data_in_disk, args=(complete_file_name, downloaded_data))\
            #     .start()
            FileUtil.save_website_data_in_disk(complete_file_name, downloaded_data)
            was_pop, popped_path = self.cache.cache_website(data_path, complete_file_name)
            if was_pop:
                file_name = FileUtil.generate_file_name(popped_path)
                complete_file_name = FileUtil.generate_file_path(Constants.FILE_DIRECTORY, file_name)
                threading.Thread(target=FileUtil.delete_website_data_from_disk, args=complete_file_name)\
                    .start()
            return LocalResponse(downloaded_data, Constants.HTTP_STATUS_CODE_OK)

        except Exception as e:
            return LocalResponse("", Constants.HTTP_NOT_FOUND_RESPONSE_CODE)
