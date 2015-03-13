# -- encoding: utf8 --
# author: TYM
# date: 2015-3-10
from urllib.parse import urljoin
import json
import requests
import config

class Channel:
    _channel = ''
    url_root = 'http://dm.tuna.moe/'
    url_exam_get = urljoin(url_root, '/api/v1/channels/{channel}/danmaku/exam')
    url_exam_post = urljoin(url_root, '/api/v1/channels/{channel}/danmaku')
    url_danmaku = urljoin(url_root, '/api/v1/channels/{channel}/danmaku')
    _get_headers = {}
    _post_headers = {'content-type': 'application/json; charset=utf8'}

    def __init__(self, channel, uuid, sub_passwd, pub_passwd=None):
        self._channel = channel
        self.url_exam_get = self.url_exam_get.format(channel=self._channel)
        self.url_exam_post = self.url_exam_post.format(channel=self._channel)
        self.url_danmaku = self.url_danmaku.format(channel=self._channel)
        self._get_headers['X-GDANMAKU-SUBSCRIBER-ID'] = uuid
        self._get_headers['X-GDANMAKU-AUTH-KEY'] = sub_passwd
        # self._post_headers['X-GDANMAKU-SUBSCRIBER-ID'] = uuid
        if pub_passwd:
            self._post_headers['X-GDANMAKU-AUTH-KEY'] = pub_passwd
        else:
            self._post_headers['X-GDANMAKU-AUTH-KEY'] = ''
        self._post_headers['X-GDANMAKU-TOKEN'] = 'APP:'


    def get_danmaku(self):
        # res = requests.get(self.url_exam_get, headers=self._get_headers)
        res = requests.get(self.url_danmaku, headers=self._get_headers)
        return json.loads(res.text)


    def post_danmaku(self, danmaku):
        if type(danmaku) == type(''):
            res = requests.post(self.url_exam_post, data=danmaku,
                    headers=self._post_headers)
        elif type(danmaku) == type({}) or type(danmaku) == type([]):
            res = requests.post(self.url_exam_post, data=json.dumps(danmaku),
                   headers=self._post_headers)
        return res.text


if __name__ == '__main__':
    import time

    c = Channel('demo', 'uuid', '', '')
    s = c.post_danmaku({'color': 'green', 'position': 'fly', 'content': '超长弹幕超长弹幕超长弹幕超长弹幕超长弹幕超长弹幕超长弹幕'})
    print(s)
    while True:
        danmaku = c.get_danmaku()
        if danmaku:
            print(danmaku)

