
import seldom


class TestRequest(seldom.TestCase):

    def start(self):
        self.url = "http://127.0.0.1:5000/add_user"

    def test_case(self):
        headers = {"Host": "127.0.0.1:5000", "User-Agent": "python-requests/2.25.0", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "Connection": "keep-alive", "Content-Length": "41", "Content-Type": "application/json"}
        cookies = {}
        self.post(self.url, json={"name": "tom", "age": 22, "height": 177}, headers=headers, cookies=cookies)
        self.assertStatusCode(200)


if __name__ == '__main__':
    seldom.main()
