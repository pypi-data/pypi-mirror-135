import seldom


class TestRequest(seldom.TestCase):

    def start(self):
        self.url = "http://127.0.0.1:5000/phone/1"

    def test_case(self):
        headers = {"Host": "127.0.0.1:5000", "User-Agent": "python-requests/2.25.0", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "Connection": "keep-alive", "Content-Length": "52", "Content-Type": "application/x-www-form-urlencoded"}
        cookies = {}
        self.put(self.url, data={"name": "\u534e\u4e3a\u624b\u673a", "price": "3999"}, headers=headers, cookies=cookies)
        self.assertStatusCode(200)


if __name__ == '__main__':
    seldom.main()
