import requests

from ssl_ch import SSLUtils
import urllib.request

class Check_site:
    def __init__(self):
        self.tool = SSLUtils()

    def get_ssl_cert(self, url):
        return self.tool.fetch_sever_sertificate_x509(url)

    def is_valid(self, url):
        try:
            requests.get(url, timeout=5)
            return True
        except Exception:
            return False

    def check_redirect(self, url):
        r = requests.get(url, verify=False)
        for i, response in enumerate(r.history, 1):
            print(i, response.url)
        if len(r.history) > 1:
            return False
        return True

# c = Check_site()
# c.new_url('http://kremlin.ru/')
# print(c.check_redirect())
# print(c.test.history)
