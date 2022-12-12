# Http client to test the server
from urllib.request import Request, urlopen

from utils.file_utils import FileUtil


class Test:
    def __init__(self, url: str):
        self.url = url

    def test(self):
        try:
            print(self.url)
            req = Request(self.url)
            response = urlopen(req)
            return response.read()
        except Exception as e:
            return ("Error: " + str(e)).encode('utf-8')


if __name__ == '__main__':
    # Download the website data from the internet.
    url = "http://localhost:25019/American_Civil_war"

        # print(url)
    test = Test(url)
    res = test.test()

