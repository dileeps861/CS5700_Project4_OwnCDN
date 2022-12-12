
# This file will save the website data in the disk.
import os
import zlib


class FileUtil:

    # Save the website data in the disk.
    @staticmethod
    def save_website_data_in_disk(website_name, web_data):
        with open(website_name, 'wb') as f:
            f.write(FileUtil.compress_website_data(web_data))

    # Get the website data from the disk.
    @staticmethod
    def get_website_data_from_disk(website_name):
        with open(website_name, 'rb') as f:
            return FileUtil.decompress_website_data(f.read())

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
    def compress_website_data(website_data):
        return zlib.compress(website_data)

    @staticmethod
    def decompress_website_data(website_data):
        return zlib.decompress(website_data)

    @staticmethod
    def create_dir_if_not_exists(dir_name):
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

    @staticmethod
    def generate_file_path(dir_name, file_name):
        return dir_name+"/"+file_name

    @staticmethod
    def generate_file_name(url_path):
        return url_path.replace('/', '_')

    @staticmethod
    def save_str_file(file_path, file_data):
        with open(file_path, 'w') as f:
            f.write(file_data)


    # Gets the size of the a given Directory
    @staticmethod
    def estimate_space():
        path = "."
        dir_size = 0
        for dir_path, dir_names, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dir_path, f)
                dir_size += os.path.getsize(fp)
        "Directory Size =" + str(dir_size)
        return dir_size

    @staticmethod
    def get_content_size(obj, st):

        return 0


