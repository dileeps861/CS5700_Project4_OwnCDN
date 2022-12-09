from collections import OrderedDict


# Cache the website data in the disk.
# The cache is implemented using least recently used algorithm.
class Cache:
    MAX_CACHE_SIZE = 180

    def __init__(self):
        self.cache = OrderedDict()
        self.cache_size = 0

    # Add a new website to the cache.
    def cache_website(self, website_name, web_data):
        self.cache[website_name] = web_data
        self.cache_size += 1
        if self.cache_size > Cache.MAX_CACHE_SIZE:
            self.remove_least_recently_used_website()

    # Remove the least recently website from the cache if the cache is full.
    def remove_least_recently_used_website(self):
        self.cache.popitem(last=False)
        self.cache_size -= 1

    # Get the website data from the cache.
    def get_website_data(self, page_name):
        page_data = self.cache[page_name]
        self.cache.move_to_end(page_name)
        return page_data

    # Get all the websites from the cache.
    def get_all_pages(self):
        return self.cache.items()
