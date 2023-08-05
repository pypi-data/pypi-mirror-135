#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :  viewModel.py
@Date    :  2021/8/17
@Author  :  Yaronzz
@Version :  1.0
@Contact :  yaronhuang@foxmail.com
@Desc    :
"""
from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal


class ViewModel(QObject):
    SIGNAL_REFRESH_VIEW = pyqtSignal(str, object)

    def __init__(self):
        super(ViewModel, self).__init__()
        self.view = None

    def show(self):
        self.view.show()

    def hide(self):
        self.view.hide()
