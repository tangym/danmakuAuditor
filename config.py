# -- encoding: utf-8 --
# author: TYM
# date: 2015-3-12
from urllib.parse import urljoin
from PyQt4 import QtCore
import logging
import logging.handlers

# constants
URL_ROOT = 'http://dm.tuna.moe/'

URL = {
    'exam_get' : urljoin(URL_ROOT, '/api/v1/channels/{channel}/danmaku/exam'),
    'exam_post' : urljoin(URL_ROOT, '/api/v1/channels/{channel}/danmaku'),
    'danmaku' : urljoin(URL_ROOT, '/api/v1/channels/{channel}/danmaku')
}

HOTKEY = {
    'yes' : [QtCore.Qt.Key_Return, ] ,
    'no' : [QtCore.Qt.Key_Escape, QtCore.Qt.Key_Space],
}

EXAM_BUTTON_MAX_SIZE = {
    'height' : 25,
    'width' : 25,
}

DANMAKU_MAX_SIZE = {
    'height': 200,
    'width': 2000,  # 400
}

DANMAKU_MIN_SIZE = {
    'height': 30, #150,
    'width': 400,
}

# logging
LOG_FILE = 'danmaku_exam_gui.log'

logger = logging.getLogger('dm_exam')
handler = logging.handlers.RotatingFileHandler(LOG_FILE, 'w', encoding='utf-8')
formatter = logging.Formatter('%(asctime)s-%(levelname)s: %(message)s')

handler.setFormatter(formatter)
logger.setLevel(logging.INFO)
logger.addHandler(handler)
