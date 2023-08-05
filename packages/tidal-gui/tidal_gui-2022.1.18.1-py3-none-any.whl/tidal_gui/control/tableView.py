#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :  tableView.py
@Date    :  2021/9/10
@Author  :  Yaronzz
@Version :  1.0
@Contact :  yaronhuang@foxmail.com
@Desc    :
"""
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QTableView, QAbstractItemView


class TableView(QTableView):
    def __init__(self, columnNames: list, rowCount: int = 20):
        super(TableView, self).__init__()

        self._model = QStandardItemModel()
        self._model.setColumnCount(len(columnNames))
        self._model.setRowCount(rowCount)

        for index, name in enumerate(columnNames):
            self._model.setHeaderData(index, Qt.Horizontal, name)

        self.setModel(self._model)
        # self.setHorizontalHeaderItem(index, QTableWidgetItem(name))
        # for index in range(0, rowCount):
        #     self.setRowHeight(index, 50)

        self.setShowGrid(False)
        self.verticalHeader().setVisible(False)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)

        self.horizontalHeader().setStretchLastSection(True)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.setFocusPolicy(Qt.NoFocus)

    def addItem(self, rowIdx: int, colIdx: int, text: str):
        item = QStandardItem(text)
        item.setTextAlignment(Qt.AlignCenter)
        self._model.setItem(rowIdx, colIdx, item)
    #
    # def addWidgetItem(self, rowIdx: int, colIdx: int, widget):
    #     self.setCellWidget(rowIdx, colIdx, widget)
