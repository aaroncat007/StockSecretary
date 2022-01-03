#!/usr/bin/python
# -*- coding:utf-8 -*-

from Services.MessageHandler import MessageHandler
from Models.StockModel import StockModel
import re

# 查詢股票資訊
class SearchStockHandler(MessageHandler):

    COMMAND_HELP = "HELP"
    COMMAND_QUERY = "QUERY"


    def __init__(self):
        super().__init__()
        self.stockModel = StockModel()

    def getMessage(self,message,handler="QUERY"):
        response = self.MESSAGE_HANDLE(handler,message)
        return response

    # 訊息處理
    def MESSAGE_HANDLE(self,COMMAND,message):    
        """
        訊息處理函式
        COMMAND: 指令
        Message: message object
        """
        
        # 使用者的telegram ID
        telegramID = message.from_user.id  
        
        # 指令判斷
        if COMMAND == self.COMMAND_QUERY:
            "查詢股票資訊"
            stockStr = message.text
            response = self.QueryStock(stockStr)
            return response
        
        elif  COMMAND == self.COMMAND_HELP:
            "取得說明"
            response = self.helpMessage()
            return response
        
        else:
            return f"未定義指令:{COMMAND}"


    def QueryStock(self,stockStr):
        """
        查詢股票資訊
        :param stockStr:股票代碼
        """
        # 進來的格式會是 /stock 股票代碼
        # 移除命令並去除空白
        stockStr = stockStr.replace('/stock','')
        stockStr = stockStr.strip()

        if stockStr == "":
            return f"請輸入股票代碼"

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


    def helpMessage(self):
        "使用說明"
        return """
*查詢股票資訊: /stock 股票代碼 
範例: 當查詢東泥資訊
/stock 1110
"""