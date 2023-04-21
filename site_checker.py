from tld import get_tld

import requests

from ssl_ch import SSLUtils


class Check_site:
    def __init__(self):
        self.tool = SSLUtils()

    def get_ssl_cert(self, url):
        return self.tool.fetch_sever_sertificate_x509(url) is not None

    def is_valid(self, url):
        try:
            if 'http' not in url:
                url = 'http://' + url

            a = requests.get(url, headers={'User-Agent': 'Chrome'}, verify=False)
            return True
        except Exception:
            return False

    def check_redirect(self, url):
        if 'http' not in url:
            url = 'http://' + url
        self.r = requests.get(url, headers={'User-Agent': 'Chrome'}, verify=False)
        for i, response in enumerate(self.r.history, 1):
            print(i, response.url)
        if len(self.r.history) > 1:
            return False
        return True

    def check_domens_levels(self, url):
        parsed = get_tld(url)

# c = Check_site()
# c.new_url('http://kremlin.ru/')
# print(c.check_redirect())
# print(c.test.history)
