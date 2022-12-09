
# This file will save the website data in the disk.
import os
import zlib


class FileUtil:

    # Save the website data in the disk.
    @staticmethod
    def save_website_data_in_disk(website_name, web_data):
        with open(website_name, 'wb') as f:
            f.write(web_data)

    # Get the website data from the disk.
    @staticmethod
    def get_website_data_from_disk(website_name):
        with open(website_name, 'rb') as f:
            return f.read()

    # Check if the website data is present in the disk.
    @staticmethod
    def is_website_data_present_in_disk(website_name):
        return os.path.isfile(website_name)

    # Delete the website data from the disk.
    @staticmethod
    def delete_website_data_from_disk(website_name):
        os.remove(website_name)
        return True

    # Delete the website data from the disk.
    @staticmethod
    def delete_all_website_data_from_disk():
        for file in os.listdir("."):
            if file.endswith(".html"):
                os.remove(file)
        return True

    @staticmethod
    def compress_website_data(website_name):
        return zlib.compress(website_name)

