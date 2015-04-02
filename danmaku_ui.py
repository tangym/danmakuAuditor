#!/usr/bin/python3
# -- encoding: utf8 --
# author: TYM
# date: 2015-4-1

import sys
import time
from threading import Thread, Lock
from PyQt4.QtGui import *
from PyQt4 import QtCore
import logging
import json
from channel import ExamChannel
import config

log = config.logger

class DanmakuLine(QWidget):
    _danmaku = {}

    def __init__(self, danmaku):
        QWidget.__init__(self)
        self.setLayout(QBoxLayout(QBoxLayout.LeftToRight))

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
        self.label.setWordWrap(True)
        self.label.setAlignment(QtCore.Qt.AlignLeft)# | QtCore.Qt.AlignTop)
        self.setMaximumSize(config.DANMAKU_MAX_SIZE['width'],
                            config.DANMAKU_MAX_SIZE['height'])
        self.setMinimumSize(config.DANMAKU_MIN_SIZE['width'],
                            config.DANMAKU_MIN_SIZE['height'])

        self.yes_button.clicked.connect(self.eject_danmaku)
        self.no_button.clicked.connect(self.delete_danmaku)

        self.layout().addWidget(self.label)
        self.layout().addWidget(self.yes_button)
        self.layout().addWidget(self.no_button)
        # 分割弹幕
        self.layout().setSpacing(1)

        # 背景填充
        #self.setAutoFillBackground(True)
        #p = self.palette()
        #p.setColor(self.backgroundRole(), QColor(200, 200, 200, 255))
        #self.setPalette(p)

    @QtCore.pyqtSlot()
    def eject_danmaku(self):
        result = self.parentWidget().parentWidget().parentWidget().parentWidget()\
                    ._channel.post_danmaku(self._danmaku)
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
        #self.add_danmaku({
        #                            'content': "aaaaaaaaaaaaaaaa",
        #                            'position': "fly",
        #                            'color': "black",
        #                        })

    def add_danmaku(self, danmaku):
        danmaku_line = DanmakuLine(danmaku)
        self.layout().addWidget(danmaku_line)

        # 将stretch保持在底部
        #spacer = self.layout().itemAt(self.layout().count() - 1)
        #if type(spacer) == type(QSpacerItem(0,0)):
        #        self.layout().removeItem(spacer)
        for i in range(self.layout().count()):
            spacer = self.layout().itemAt(i)
            if type(spacer) == type(QSpacerItem(0,0)):
                self.layout().takeAt(i)

        # 将弹幕保持在顶部
        self.layout().addStretch()

        # self.adjustSize()

    def count(self):
        cnt = 0
        for i in range(self.layout().count()):
            spacer = self.layout().itemAt(i)
            if type(spacer) != type(QSpacerItem(0,0)):
                cnt += 1
        return cnt


class TopWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setLayout(QBoxLayout(QBoxLayout.LeftToRight))

        self.start_button = QPushButton("继续")
        self.pause_button = QPushButton("暂停")
        self.layout().addWidget(QLabel("提示：Enter为审核通过，Esc为不通过", self))
        self.layout().addWidget(self.start_button)
        self.layout().addWidget(self.pause_button)
        self.start_button.hide()

        self.pause_button.clicked.connect(self.on_pause_button_clicked)
        self.start_button.clicked.connect(self.on_start_button_clicked)

    @QtCore.pyqtSlot()
    def on_pause_button_clicked(self):
        self.pause_button.hide()
        self.start_button.show()

    @QtCore.pyqtSlot()
    def on_start_button_clicked(self):
        self.pause_button.show()
        self.start_button.hide()


class DanmakuExamWidget(QWidget):
    _channel = None
    channel_widget = None
    _danmakus = []
    _lock = Lock()
    _danmaku_got = QtCore.pyqtSignal()
    _danmaku_eject = QtCore.pyqtSignal(int, name='_danmaku_eject')
    _danmaku_delete = QtCore.pyqtSignal(int, name='_danmaku_delete')

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setLayout(QBoxLayout(QBoxLayout.TopToBottom))
        self._closed = False

        self.top_widget = TopWidget(self)
        self.layout().addWidget(self.top_widget)

        self.danmaku_widget = DanmakuWidget()
        self.danmaku_scroll_area = QScrollArea(self)
        #self.danmaku_scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.danmaku_scroll_area.setWidget(self.danmaku_widget)
        self.layout().addWidget(self.danmaku_scroll_area)

        self.resize(500, 500)

        self._danmaku_got.connect(self.add_danmaku)
        self._danmaku_eject.connect(self.eject_danmaku)
        self._danmaku_delete.connect(self.delete_danmaku)

    def get_danmakus(self):
        if self._channel:
            while not self._closed:
                if self.top_widget.start_button.isHidden():
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
            danmaku_line.eject_danmaku()
        except AttributeError as e:
            log.error('no more danmakus. %s' % repr(e))
            return

    def closeEvent(self, event):
        self._closed = True
        if self.danmaku_widget.count():
            # TODO: dialogue window
            button = QMessageBox.warning(self, '注意', '放弃剩余弹幕？', QMessageBox.No, QMessageBox.Yes)
            if button == QMessageBox.Yes:
                self.setParent(None)
            elif button == QMessageBox.No:
                event.ignore()
                return
            else:
                # TODO: Throw exception
                self.ignore()
                return
        else:
            pass
        self.channel_widget.setGeometry(self.x(), self.y(),
                self.channel_widget.width(), self.channel_widget.height())
        self.channel_widget.show()

    def resizeEvent(self, event):
        w = self.danmaku_scroll_area.width() * 0.95
        h = self.danmaku_scroll_area.height() * 0.95
        self.danmaku_widget.adjustSize()
        self.danmaku_widget.resize(w, h if h > self.danmaku_widget.height()
                else self.danmaku_widget.height())

    def keyPressEvent(self, event):
        if event.key() == config.HOTKEY['yes']:
            self._danmaku_eject.emit(0)
        elif event.key() == config.HOTKEY['no']:
            self._danmaku_delete.emit(0)
