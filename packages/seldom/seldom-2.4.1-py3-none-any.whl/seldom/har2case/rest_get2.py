import seldom


class TestRequest(seldom.TestCase):

    def start(self):
        self.url = "http://127.0.0.1:5000/search/"

    def test_case(self):
        headers = {"Host": "127.0.0.1:5000", "User-Agent": "python-requests/2.25.0", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "Connection": "keep-alive"}
        cookies = {}
        self.get(self.url, params={"q": "selenium"}, headers=headers, cookies=cookies)
        self.assertStatusCode(200)
        self.delete()


if __name__ == '__main__':
    seldom.main()
