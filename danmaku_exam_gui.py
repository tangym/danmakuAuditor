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
import config

class InputWidget(QWidget):
    def __init__(self, label='', line_edit=''):
        QWidget.__init__(self)
        self.label = QLabel(label)
        self.line_edit = QLineEdit(line_edit)
        self.setLayout(QBoxLayout(QBoxLayout.LeftToRight))
        self.layout().addWidget(self.label)
        self.layout().addWidget(self.line_edit)


class DanmakuLine(QWidget):
    _danmaku = {}

    def __init__(self, danmaku):
        QWidget.__init__(self)

        self._danmaku = danmaku
        self.label = QLabel(self._danmaku['content'])
        self.yes_button = QPushButton('√')
        self.no_button = QPushButton('×')

        # self.yes_button.setStyleSheet('background-color: green')
        # self.no_button.setStyleSheet('background-color: red')
        self.label.setStyleSheet('color: %s' % self._danmaku['color'])
        self.yes_button.setMaximumSize(config.EXAM_BUTTON_MAX_SIZE['width'],
                                       config.EXAM_BUTTON_MAX_SIZE['height'])
        self.no_button.setMaximumSize(config.EXAM_BUTTON_MAX_SIZE['width'],
                                       config.EXAM_BUTTON_MAX_SIZE['height'])
        self.label.setMaximumSize(config.DANMAKU_MAX_SIZE['width'],
                                  config.DANMAKU_MAX_SIZE['height'])
        self.label.setWordWrap(True)
        self.label.setAlignment(QtCore.Qt.AlignLeft)# | QtCore.Qt.AlignTop)

        self.yes_button.clicked.connect(self.eject_danmaku)
        self.no_button.clicked.connect(self.delete_danmaku)

        self.setLayout(QBoxLayout(QBoxLayout.LeftToRight))
        self.layout().addWidget(self.label)
        self.layout().addWidget(self.yes_button)
        self.layout().addWidget(self.no_button)


    @QtCore.pyqtSlot()
    def eject_danmaku(self):
        result = self.parentWidget().parentWidget()._channel.post_danmaku(self._danmaku)
        try:
            json.loads(result)
        except ValueError as e:
            log.error('posting %s fails. %s - %s' %
                    (json.dumps(danmaku_line._danmaku), result, repr(e)))
            return
        log.info('eject %s' % json.dumps(self._danmaku))
        self.setParent(None)


    @QtCore.pyqtSlot()
    def delete_danmaku(self):
        log.info('delete %s' % json.dumps(self._danmaku))
        self.setParent(None)


class DanmakuWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setLayout(QBoxLayout(QBoxLayout.TopToBottom))


    def add_danmaku(self, danmaku):
        danmaku_line = DanmakuLine(danmaku)
        self.layout().addWidget(danmaku_line)


class ExamWidget(QWidget):
    _channel = None
    _danmakus = []
    _lock = Lock()
    _danmaku_got = QtCore.pyqtSignal()
    _danmaku_eject = QtCore.pyqtSignal(int, name='_danmaku_eject')
    _danmaku_delete = QtCore.pyqtSignal(int, name='_danmaku_delete')

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
        self.danmaku_widget = DanmakuWidget()

        self.uuid_widget.button.clicked.connect(lambda :
                self.uuid_widget.line_edit.setText(sid.shorten(uuid.uuid1().bytes)))
        self.connect_button.clicked.connect(self.connect_channel)
        self._danmaku_got.connect(self.add_danmaku)

        self._danmaku_eject.connect(self.eject_danmaku)
        self._danmaku_delete.connect(self.delete_danmaku)

        self.setLayout(QBoxLayout(QBoxLayout.TopToBottom))
        self.layout().addWidget(self.channel_widget)
        self.layout().addWidget(self.pub_passwd_widget)
        self.layout().addWidget(self.exam_passwd_widget)
        self.layout().addWidget(self.uuid_widget)
        self.layout().addWidget(self.connect_button)
        self.layout().addWidget(self.danmaku_widget)

        self.setWindowTitle('弹幕审核')


    @QtCore.pyqtSlot()
    def connect_channel(self):
        channel_name = self.channel_widget.line_edit.text().strip()
        pub_passwd = self.pub_passwd_widget.line_edit.text().strip()
        exam_passwd = self.exam_passwd_widget.line_edit.text().strip()
        uid = self.uuid_widget.line_edit.text().strip()

        self._channel = ExamChannel(channel_name, uid, exam_passwd,
                                    pub_passwd=pub_passwd)
        thread = Thread(target=self.get_danmakus, daemon=True)
        thread.start()


    def get_danmakus(self):
        if self._channel:
            while True:
                danmakus = self._channel.get_danmaku()
                if danmakus:
                    self._lock.acquire()
                    self._danmakus = \
                            [{
                                'content': danmaku['text'],
                                'position': danmaku['position'],
                                'color': danmaku['style']
                            } for danmaku in danmakus]
                    self._lock.release()
                    self._danmaku_got.emit()


    @QtCore.pyqtSlot()
    def add_danmaku(self):
        self._lock.acquire()
        if self._danmakus:
            for danmaku in self._danmakus:
                self.danmaku_widget.add_danmaku(danmaku)
        self._danmakus = []
        self._lock.release()


    def keyPressEvent(self, event):
        if event.key() == config.HOTKEY['yes']:
            self._danmaku_eject.emit(0)
        elif event.key() == config.HOTKEY['no']:
            self._danmaku_delete.emit(0)


    @QtCore.pyqtSlot(int, name='delete_danmaku')
    def delete_danmaku(self, index):
        try:
            danmaku_line = self.danmaku_widget.layout().itemAt(index).widget()
        except AttributeError as e:
            log.error('no more danmakus. %s' % repr(e))
            return
        # self.danmaku_widget.layout().removeWidget(danmaku_line)
        danmaku_line.delete_danmaku()


    @QtCore.pyqtSlot(int, name='eject_danmaku')
    def eject_danmaku(self, index):
        try:
            danmaku_line = self.danmaku_widget.layout().itemAt(index).widget()
        except AttributeError as e:
            log.error('no more danmakus. %s' % repr(e))
            return

        #self.layout().removeWidget(danmaku_line)
        danmaku_line.eject_danmaku()


if __name__ == '__main__':
    log = config.logger

    app = QApplication(sys.argv)
    main = ExamWidget()
    main.show()

    sys.exit(app.exec_())
