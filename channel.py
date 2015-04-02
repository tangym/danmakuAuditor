# -- encoding: utf-8 --
# author: TYM
# date: 2015-3-10
from urllib.parse import urljoin
import json
import requests
import config

class Channel:
    url_get = config.URL['danmaku']
    url_post = config.URL['exam_post']

    _channel = ''
    _get_headers = {}
    _post_headers = {'content-type': 'application/json; charset=utf8'}

    def __init__(self, channel, uuid, sub_passwd=None, pub_passwd=None):
        self._channel = channel
        self.url_get = self.url_get.format(channel=self._channel)
        self.url_post = self.url_post.format(channel=self._channel)

        self._get_headers['X-GDANMAKU-SUBSCRIBER-ID'] = uuid
        self._get_headers['X-GDANMAKU-AUTH-KEY'] = \
                    sub_passwd if sub_passwd else ''
        # self._post_headers['X-GDANMAKU-SUBSCRIBER-ID'] = uuid
        self._post_headers['X-GDANMAKU-AUTH-KEY'] = \
                    pub_passwd if pub_passwd else ''
        self._post_headers['X-GDANMAKU-TOKEN'] = 'APP:'


    def get_danmaku(self):
        res = requests.get(self.url_get, headers=self._get_headers)
        try:
            #print(res.text)
            return json.loads(res.text)
        except ValueError as e:
            return {}


    def post_danmaku(self, danmaku):
        if type(danmaku) == type(''):
            res = requests.post(self.url_post, data=danmaku,
                    headers=self._post_headers)
        elif type(danmaku) == type({}) or type(danmaku) == type([]):
            res = requests.post(self.url_post, data=json.dumps(danmaku),
                   headers=self._post_headers)
        return res.text


class ExamChannel(Channel):
    url_get = config.URL['exam_get']
    url_post = config.URL['exam_post']

    def __init__(self, channel, uuid, exam_passwd, sub_passwd=None,
                    pub_passwd=None):
        Channel.__init__(self, channel, uuid, sub_passwd, pub_passwd)

        self._get_headers['X-GDANMAKU-AUTH-KEY'] = exam_passwd
        self._post_headers['X-GDANMAKU-EXAM-KEY'] = exam_passwd



if __name__ == '__main__':
    import time

    #c = ExamChannel('demo', 'uuid', '', '')
    #c = ExamChannel('cIemo', 'uuid', '000000', sub_passwd='000000')
    s = c.post_danmaku({'color': 'green', 'position': 'fly', 'content': '超长弹幕超长弹幕超长弹幕超长弹幕超长弹幕超长弹幕超长弹幕'})
    print(s)
    while True:
        danmaku = c.get_danmaku()
        if danmaku:
            print(danmaku)

