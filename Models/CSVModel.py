#!/usr/bin/python
# -*- coding:utf-8 -*-

from Models.dbModel import dbModel

# CSV 資料庫
class CSVModel(dbModel):

    def __init__(self):
        super().__init__()

    def initTable(self):
        return NotImplemented

    #取得大盤資訊
    def getTWStock(self):
        return """\
加權指數 0000
17812.59 ▲26.85 0.15%
開盤 17744.54
昨收 17785.74
最高 17822.74
最低 17718.27
成交量(億) 3,459.2
預估量(億) 3,459\
"""