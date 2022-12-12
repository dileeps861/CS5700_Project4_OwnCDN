
import os
import sqlite3
import sys
import zlib



class CacheWithDB:
    def __init__(self):
        self.max_capacity = 15000000
        self.connection = sqlite3.connect("websites.db", check_same_thread=False)
        self.db_connection_executor = self.connection.cursor()
        self.db_connection_executor.execute('''CREATE TABLE IF NOT EXISTS websites(content_path TEXT primary key, content BLOB, frequency_count INT, data_size INT);''')


    def is_website_present_in_cache(self, path):
        self.db_connection_executor.execute("SELECT * FROM websites WHERE content_path = :content_path", {"content_path": path})
        data = self.db_connection_executor.fetchone()
        return data is not None

    def close(self):
        self.connection.commit()
        self.connection.close()

    def get_cache_size(self):
        return os.stat('websites.db').st_size

    def is_full(self, data):
        cache_size = self.get_cache_size()
        return cache_size + sys.getsizeof(data) > self.max_capacity

    def cache_website(self, path, data):
        compressed_data = zlib.compress(data)
        size = sys.getsizeof(compressed_data)
        frequency_count = 1
        if self.is_full(compressed_data):
            self.remove_least_priority_data(sys.getsizeof(compressed_data))

        self.db_connection_executor.execute("INSERT INTO websites(content_path,content,frequency_count,data_size)VALUES(?,?,?,?)",
                                            (path, compressed_data, frequency_count, size))
        self.connection.commit()

    def remove_least_priority_data(self, file_size):
        #  Keep removing the least priority data until the cache size is less than the maximum capacity - data_size.
        #  The least priority data is the one with the least frequency count.
        while self.get_cache_size() + file_size >= self.max_capacity:
            self.db_connection_executor.execute(
                "DELETE FROM websites WHERE Path in (SELECT content_path FROM websites WHERE frequency_count = (SELECT MIN(frequency_count) FROM websites))")
            self.connection.commit()
            self.db_connection_executor.execute("VACUUM")

    def get_cached_website(self, path):
        self.db_connection_executor.execute("SELECT * FROM websites WHERE content_path = :content_path", {"content_path": path})
        data = self.db_connection_executor.fetchone()
        if data is not None:
            content = zlib.decompress(data[1])
            frequency_count = data[2]
            frequency_count += 1
            self.db_connection_executor.execute("UPDATE websites SET frequency_count =:frequency_count WHERE content_path=:content_path",
                                                {"frequency_count": frequency_count, "content_path": path})
            self.connection.commit()
            return content
        return None