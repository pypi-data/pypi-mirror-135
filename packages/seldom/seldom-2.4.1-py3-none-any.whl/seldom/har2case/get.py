import seldom


class TestRequest(seldom.TestCase):

    def start(self):
        self.url = "http://127.0.0.1:8000/api/get_event_list/?eid=1"

    def test_case(self):
        headers = {"Host": "127.0.0.1:8000", "User-Agent": "python-requests/2.25.0", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "Connection": "keep-alive"}
        cookies = {}
        self.get(self.url, params={"eid": "1"}, headers=headers, cookies=cookies)
        self.assertStatusCode(200)


if __name__ == '__main__':
    seldom.main()
