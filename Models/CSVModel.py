#!/usr/bin/python
# -*- coding:utf-8 -*-


from Models.dbModel import dbModel

# CSV 資料庫
class CSVModel(dbModel):

    def __init__(self):
        super().__init__()

    #取得使用者名稱
    def getUser(self,userID):
        if userID == 1092487471:
            return "Aaron"
        return "Guest"

    #取得股票基本資訊
    def getStock(self,stockID):
        return {
            '1101': '1101-台泥',
            '1102': '1102-亞泥',
            '1103': '1103-嘉泥',
            '1104': '1104-環泥',
            '1107': '1107-建台',
            '1109': '1109-信大',
            '1110': '1110-東泥',
        }.get(stockID,'NotFound')

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