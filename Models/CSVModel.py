#!/usr/bin/python
# -*- coding:utf-8 -*-

from Models.dbModel import dbModel

# CSV 資料庫
class CSVModel(dbModel):

    def __init__(self):
        super().__init__()

    def initTable(self):
        return NotImplemented