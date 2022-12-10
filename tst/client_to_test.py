# Http client to test the server
from urllib.request import Request, urlopen

from utils.file_utils import FileUtil


class Test:
    def __init__(self, url: str):
        self.url = url

    def test(self):
        headers_dict = {'Accept-Language': 'en-IN,en-US;q=0.9,en;q=0.8,hi-IN;q=0.7,hi;q=0.6,en-GB;q=0.5',
                        'Accept-Encoding': "utf-8",
                        'accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9, image / avif, '
                                  'image / webp, image / apng, * / *;q = 0.8, application / signed - exchange;v = b3;q '
                                  '= 0.9', 'Connection': 'keep-alive', 'path': '/wiki/Creational_pattern'}
        req = Request(url, headers=headers_dict)
        response = urlopen(req)
        return response.read()


if __name__ == '__main__':
    # Download the website data from the internet.
    url = "http://localhost:7566/YouTube"
    test = Test(url)
    FileUtil.save_str_file('index.html', test.test().decode("utf-8"))
