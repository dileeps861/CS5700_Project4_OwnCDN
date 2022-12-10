"""
Get the file name from the url
"""


# Get the file name from the url. If the url does not contain a file name, return 'index.html' as default file name
def get_file_name_from_url(url):
    if check_url_contains_file(url):
        return url.split('/')[-1]
    else:
        return 'index.html'


# Get the file extension from the url
def get_file_extension_from_url(url):
    return url.split('.')[-1]


# Check if the url is valid
def check_url(url):
    return url is None or url.startswith('http://') or url.startswith('ftp://') \
           or url.startswith('ftps://') or url.startswith('sftp://') or url.startswith('smb://') \
           or url.startswith('smb://') or url.startswith('file://') or url.startswith('www.') \
           or url.startswith('https://')


# Check if the url is a file with extension
def check_url_contains_file(url):
    return '.' in url.split('/')[-1]


class URL:
    def __init__(self, url):
        self.url = url
        self.protocol = None
        self.domain = None
        self.path = None
        self.file_name = None
        self.file_extension = None
        self.parse_url()

    def parse_url(self):
        self.protocol = self.url.split('://')[0]
        self.domain = self.url.split('://')[1].split('/')[0]
        self.path = self.url.split('://')[1].split('/')[1:]

        if len(self.path) == 0 or self.path[-1] == '':
            self.path = '/'
            self.file_name = 'index.html'
        else:
            self.file_name = self.path[-1]
            self.path = '/'.join(self.path)
            self.path = '/'+self.path
        self.file_extension = self.file_name.split('.')[-1]

    def get_protocol(self):
        return self.protocol

    def get_domain(self):
        return self.domain

    def get_path(self):
        return self.path

    def get_file_name(self):
        return self.file_name

    def get_file_extension(self):
        return self.file_extension

    def get_url(self):
        return self.url

    def __str__(self):
        return self.url

    def __repr__(self):
        return self.url
