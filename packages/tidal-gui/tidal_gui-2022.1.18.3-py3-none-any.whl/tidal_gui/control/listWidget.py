#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :  listWidget.py
@Date    :  2021/8/17
@Author  :  Yaronzz
@Version :  1.0
@Contact :  yaronhuang@foxmail.com
@Desc    :
"""
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QWidget

from tidal_gui.style import ListWidgetStyle


class ListWidget(QListWidget):
    def __init__(self, style: ListWidgetStyle = ListWidgetStyle.Default):
        super(ListWidget, self).__init__()
        self.setObjectName(style.name + "ListWidget")

    def addIConTextItem(self, iconUrl: str, text: str):
        self.addItem(QListWidgetItem(QIcon(iconUrl), text))

    def addWidgetItem(self, widget: QWidget):
        item = QListWidgetItem(self)
        # item.setSizeHint(QSize(widget.width(), widget.height()))
        self.addItem(item)
        self.setItemWidget(item, widget)

    def setAdjustMode(self):
        self.setResizeMode(QListWidget.Adjust)
