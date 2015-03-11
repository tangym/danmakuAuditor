#!/usr/bin/python3
# -- encoding: utf8 --
# author: TYM
# date: 2015-3-10
import sys
import time
from threading import Thread, Lock
from PyQt4.QtGui import *
from PyQt4 import QtCore
import uuid
from channel import Channel
import shorten_id as sid


# 使用62进制表示下面生成的字符串，然后转成大小写字母和数字即可。
# uuid.uuid1(node=uuid.getnode())返回32位字符（表示的16进制数），getnode()函数获取mac地址。

# c = Channel('demo', '', '')

class InputWidget(QWidget):
    def __init__(self, label='', line_edit=''):
        QWidget.__init__(self)
        self.label = QLabel(label)
        self.line_edit = QLineEdit(line_edit)
        self.setLayout(QBoxLayout(QBoxLayout.LeftToRight))
        self.layout().addWidget(self.label)
        self.layout().addWidget(self.line_edit)


class ExamWidget(QWidget):
    _danmakus = []
    _lock = Lock()
    _dmgot = QtCore.pyqtSignal()

    def __init__(self):
        QMainWindow.__init__(self)

        self.channel_widget = InputWidget(label='频道', line_edit='demo')
        self.pub_passwd_widget = InputWidget(label='密码', line_edit='')
        self.pub_passwd_widget.line_edit.setEchoMode(QLineEdit.Password)
        self.uuid_widget = InputWidget(label='uuid',
                line_edit=sid.shorten(uuid.uuid1().bytes))
        self.uuid_widget.button = QPushButton('生成')
        self.uuid_widget.layout().addWidget(self.uuid_widget.button)
        self.uuid_widget.button.clicked.connect(lambda :
                self.uuid_widget.line_edit.setText(sid.shorten(uuid.uuid1().bytes)))
        self.connect_button = QPushButton('走你')
        self.connect_button.clicked.connect(self.connect_channel)

        self.setLayout(QBoxLayout(QBoxLayout.TopToBottom))
        self.layout().addWidget(self.channel_widget)
        self.layout().addWidget(self.pub_passwd_widget)
        self.layout().addWidget(self.uuid_widget)
        self.layout().addWidget(self.connect_button)

        self._dmgot.connect(self.display_danmaku)

    def connect_channel(self):
        channel_name = self.channel_widget.line_edit.text().strip()
        pub_passwd = self.pub_passwd_widget.line_edit.text().strip()
        uid = self.uuid_widget.line_edit.text().strip()
        self.channel = Channel(channel_name, uid, pub_passwd)

        thread = Thread(target=self.get_danmakus, daemon=True)
        thread.start()

    def display_danmaku(self):
        self._lock.acquire()
        if self._danmakus:
            for danmaku in self._danmakus:
                self.layout().addWidget(QLabel(danmaku['text']))
            danmakus = []
        self._lock.release()

    def get_danmakus(self):
        while True:
            danmakus = self.channel.get_danmaku()
            if danmakus:
                self._lock.acquire()
                self._danmakus = danmakus
                self._lock.release()
                self._dmgot.emit()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = ExamWidget()
    main.show()

    sys.exit(app.exec_())


