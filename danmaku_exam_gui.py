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
import logging
import json
from channel import ExamChannel
import shorten_id as sid
from danmaku_ui import DanmakuExamWidget
import config

class InputWidget(QWidget):
    def __init__(self, label='', line_edit=''):
        QWidget.__init__(self)
        self.label = QLabel(label)
        self.line_edit = QLineEdit(line_edit)
        self.setLayout(QBoxLayout(QBoxLayout.LeftToRight))
        self.layout().addWidget(self.label)
        self.layout().addWidget(self.line_edit)


class ExamWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.channel_widget = InputWidget(label='频道', line_edit='demo')
        self.pub_passwd_widget = InputWidget(label='发布密码', line_edit='')
        self.pub_passwd_widget.line_edit.setEchoMode(QLineEdit.Password)
        self.exam_passwd_widget = InputWidget(label='审核密码', line_edit='')
        self.exam_passwd_widget.line_edit.setEchoMode(QLineEdit.Password)
        self.uuid_widget = InputWidget(label='uuid',
                line_edit=sid.shorten(uuid.uuid1().bytes))
        self.uuid_widget.button = QPushButton('生成')
        self.uuid_widget.layout().addWidget(self.uuid_widget.button)
        self.connect_button = QPushButton('走你')
        #self.danmaku_widget = DanmakuWidget()

        self.uuid_widget.button.clicked.connect(lambda :
                self.uuid_widget.line_edit.setText(sid.shorten(uuid.uuid1().bytes)))
        self.connect_button.clicked.connect(self.connect_channel)

        self.setLayout(QBoxLayout(QBoxLayout.TopToBottom))
        self.layout().addWidget(self.channel_widget)
        self.layout().addWidget(self.pub_passwd_widget)
        self.layout().addWidget(self.exam_passwd_widget)
        self.layout().addWidget(self.uuid_widget)
        self.layout().addWidget(self.connect_button)
        #self.layout().addWidget(self.danmaku_widget)

        self.setWindowTitle('弹幕审核')

    @QtCore.pyqtSlot()
    def connect_channel(self):
        channel_name = self.channel_widget.line_edit.text().strip()
        pub_passwd = self.pub_passwd_widget.line_edit.text().strip()
        exam_passwd = self.exam_passwd_widget.line_edit.text().strip()
        uid = self.uuid_widget.line_edit.text().strip()

        self.main_window = DanmakuExamWidget()
        self.main_window.channel_widget = self
        self.main_window.setGeometry(self.x(), self.y(),
                self.main_window.width(), self.main_window.height())
        self.main_window.show()
        self.hide()
        self.main_window._channel = ExamChannel(channel_name, uid, exam_passwd,
                                    pub_passwd=pub_passwd)
        thread = Thread(target=self.main_window.get_danmakus, daemon=True)
        thread.start()


if __name__ == '__main__':
    log = config.logger

    app = QApplication(sys.argv)
    main = ExamWidget()
    main.show()

    sys.exit(app.exec_())
