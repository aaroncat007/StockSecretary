#!/usr/bin/python
# -*- coding:utf-8 -*-

from Services.MessageHandler import MessageHandler
from Models.StockModel import StockModel
import re

# 查詢股票資訊
class SearchStockHandler(MessageHandler):

    def __init__(self):
        super().__init__()
        self.stockModel = StockModel()

    def getMessage(self,stockStr):

        # 進來的格式會是 /stock 股票代碼
        # 移除命令並去除空白
        stockStr = stockStr.replace('/stock','')
        stockStr = stockStr.strip()

        # 查詢資料庫
        queryResult = self.stockModel.getStockByCode(stockStr)

        if queryResult == None :
            return f"查無股票資訊:{stockStr}"
        
        #回覆訊息範本
        resultMessage = """
股票代碼:{stockCode}
股票名稱:{stockName}
市場別:{market}
證券別:{issuetype}
產業別:{industry}
發行日:{offerTime}
        """

        #正規式替換內容
        resultMessage = re.sub(r'{stockCode}',queryResult[1],resultMessage)
        resultMessage = re.sub(r'{stockName}',queryResult[2],resultMessage)
        resultMessage = re.sub(r'{market}',queryResult[3],resultMessage)
        resultMessage = re.sub(r'{issuetype}',queryResult[4],resultMessage)
        resultMessage = re.sub(r'{industry}',queryResult[5],resultMessage)
        resultMessage = re.sub(r'{offerTime}',queryResult[6],resultMessage)

        return resultMessage