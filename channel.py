# -- encoding: utf8 --
# author: TYM
# date: 2015-3-10

from urllib.parse import urljoin
import json
import requests

class Channel:
    _channel = ''
    url_root = 'http://dm.tuna.moe/'
    url_exam_get = urljoin(url_root, '/api/v1/channels/{channel}/danmaku/exam')
    url_exam_post = urljoin(url_root, '/api/v1/channels/{channel}/danmaku')
    url_danmaku = urljoin(url_root, '/api/v1/channels/{channel}/danmaku')
    _get_headers = {}
    _post_headers = {}

    def __init__(self, channel, sub_passwd, pub_passwd=None):
        self._channel = channel
        self.url_exam_get = self.url_exam_get.format(channel=self._channel)
        self.url_exam_post = self.url_exam_post.format(channel=self._channel)
        self.url_danmaku = self.url_danmaku.format(channel=self._channel)
        self._get_headers['X-GDANMAKU-SUBSCRIBER-ID'] = '123456'
        self._get_headers['X-GDANMAKU-AUTH-KEY'] = sub_passwd
        if pub_passwd:
            self._post_headers['X-GDANMAKU-AUTH-KEY'] = pub_passwd
        self._post_headers['X-GDANMAKU-TOKEN'] = 'APP:'

    def get_danmaku(self):
        res = requests.get(self.url_danmaku, headers=self._get_headers)
        return json.loads(res.text)


if __name__ == '__main__':
    import time

    #c = Channel('just_a_test', ' ')
    c = Channel('demo', '')
    #c = Channel('i_dont_know_why_cannt_i_get_danmaku', '000000')

    while True:
        danmaku = c.get_danmaku()
        if danmaku:
            print(danmaku)

