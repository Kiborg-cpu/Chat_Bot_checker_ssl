import certifi
import requests


class Check_site:
    def __init__(self, url):
        try:
            print('Проверка ssl сертифика')
            self.test = requests.get(url, headers={'User-Agent': 'Google Chrome'}, verify=certifi.where(),
                                     allow_redirects=True)
            self.has_https = True
            print('Connection OK.')
        except requests.exceptions.SSLError as err:
            print('SSL Error. Adding custom certs to Certifi store...')

    def check_redirect(self):
        if len(self.test.history) > 1:
            return True
        return False


k = Check_site('https://www.google.com/url?q=https://en.wikipedia.org/wiki/Turtle&sa=U&ved=0ahUKEwja'
               '-oaO7u3XAhVMqo8KHYWWCp4QFggVMAA&usg=AOvVaw31hklS09NmMyvgktL1lrTN')
print(k.check_redirect())
print(k.test.history)
