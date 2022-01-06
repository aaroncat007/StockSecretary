#!/usr/bin/python
# -*- coding:utf-8 -*-

from datetime import datetime
from numpy import datetime_as_string, round_
from Services.MessageHandler import MessageHandler
from Models.StockModel import StockModel
import re

# 查詢股票資訊
class SearchStockHandler(MessageHandler):

    COMMAND_HELP = "HELP"
    COMMAND_QUERY = "QUERY"
    COMMAND_GETNOW = "GETNOW"
    COMMAND_GETPE= "GETPE"
    COMMAND_GETK = "GETK"
    COMMAND_GETBIG = "GETBIG"


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

        elif  COMMAND == self.COMMAND_GETNOW:
            "取得及時"
            stockStr = message.text
            response = self.QueryStockNOW(stockStr)
            return response

        elif  COMMAND == self.COMMAND_GETPE:
            "取得日本益比資訊"#(新增)
            stockStr = message.text
            response = self.QueryStock_PE(stockStr)
            return response
        elif  COMMAND == self.COMMAND_GETK:
            "取得k值資料"#(新增)
            stockStr = message.text
            response = self.QueryStock_K(stockStr)
            return response
        elif COMMAND == self.COMMAND_GETBIG:
            "取得大股東資料"
            stockStr = message.text
            response = self.QueryStock_Big(stockStr)
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

    def QueryStockNOW(self,stockStr):
        """
        查詢股票資訊
        :param stockStr:股票代碼
        """
        # 進來的格式會是 /stock 股票代碼
        # 移除命令並去除空白
        stockStr = stockStr.replace('/q','')
        stockStr = stockStr.strip()

        if stockStr == "":
            return f"請輸入股票代碼"

       # 查詢股票資料資料庫
        StockResult = self.stockModel.getStockByCode(stockStr)

        if StockResult == None :
            return f"查無股票資訊:{stockStr}"

        # 查詢資料庫
        queryResult = self.stockModel.getStockData_Now(stockStr)

        if queryResult == None :
            return f"查無股票資訊:{stockStr}"

        #其他指標
        #col = [stockStr]
        #otherResult = self.stockModel.ger_value(col)

        #if otherResult == None :
        #    return f"查無股票資訊:{stockStr}"

        #print(otherResult)

        now = datetime.now()
        date_time = now.strftime("%Y/%m/%d %H:%M:%S")
        
        #回覆訊息範本
        resultMessage = """
股票代號    {stockCode}
股票名稱    {stockName}
時間        {timestamp}
即時價格    {stockprice}

"""
#正規式替換內容
        resultMessage = re.sub(r'{stockCode}',StockResult[1],resultMessage)
        resultMessage = re.sub(r'{stockName}',StockResult[2],resultMessage)
        resultMessage = re.sub(r'{timestamp}',date_time,resultMessage)
        resultMessage = re.sub(r'{stockprice}',str(round(queryResult,2)),resultMessage)

        return resultMessage

    def QueryStock_PE(self,stockStr):
        """
        查詢日本益比資訊
        :param stockStr:股票代碼
        """
        # 進來的格式會是 /stock 股票代碼
        # 移除命令並去除空白
        stockStr = stockStr.replace('/PE','')
        stockStr = stockStr.strip()

        if stockStr == "":
            return f"請輸入股票代碼"

       # 查詢股票資料資料庫
        StockResult = self.stockModel.getStockByCode(stockStr)

        if StockResult == None :
            return f"查無股票資訊:{stockStr}"

        # 查詢資料庫
        # 日本益比查詢日期
        now = datetime.now()
        date_time = now.strftime("%Y%m%d")
        responseResult = self.stockModel.Geronth_dateper(date_time,stockStr)

        if StockResult == None :
            return f"查無股票日本益比資訊:{stockStr}"

        lastData = responseResult.iloc[-1]

        #回覆訊息範本
        resultMessage = """
==個股日本益比查詢結果==
股票代號    {stockCode}
股票名稱    {stockName}
日期        {data1}
殖利率(%)          {data2}
股利年度             {data3}
本益比            {data4}
股價淨值比           {data5}
財報年/季          {data6}
        """
#正規式替換內容
        resultMessage = re.sub(r'{stockCode}',StockResult[1],resultMessage)
        resultMessage = re.sub(r'{stockName}',StockResult[2],resultMessage)
        resultMessage = re.sub(r'{data1}',lastData['日期'],resultMessage)
        resultMessage = re.sub(r'{data2}',lastData['殖利率(%)'],resultMessage)        
        resultMessage = re.sub(r'{data3}',lastData['股利年度'],resultMessage)
        resultMessage = re.sub(r'{data4}',lastData['本益比'],resultMessage)
        resultMessage = re.sub(r'{data5}',lastData['股價淨值比'],resultMessage)
        resultMessage = re.sub(r'{data6}',lastData['財報年/季'],resultMessage)

        return resultMessage



    def QueryStock_K(self,stockStr):
        """
        查詢股票K線今日走勢圖資訊
        :param stockStr:股票代碼
        """
        # 進來的格式會是 /stock 股票代碼
        # 移除命令並去除空白
        stockStr = stockStr.replace('/K','')
        stockStr = stockStr.strip()
        
        if stockStr == "":
            return f"請輸入股票代碼"

       # 查詢股票資料資料庫
        StockResult = self.stockModel.getStockByCode(stockStr)

        if StockResult == None :
            return f"查無股票資訊:{stockStr}"

        # 查詢資料庫
        image = self.stockModel.Get_todayK_line(stockStr)
        
        #bot.send_message(chat_id=TELEGRAM_CHAT_ID, text="K線今日走勢圖")
        #bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=data)
        #bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=open(path, 'rb'))
        
        if image == None :
            return f"str",f"查詢失敗:{stockStr}"

        return "img",image

    def QueryStock_Big(self,stockStr):
        """
        查詢股票大股東資訊
        :param stockStr:股票代碼
        """
        # 進來的格式會是 /stock 股票代碼
        # 移除命令並去除空白
        stockStr = stockStr.replace('/big','')
        stockStr = stockStr.strip()
        
        if stockStr == "":
            return f"請輸入股票代碼"

       # 查詢股票資料資料庫
        StockResult = self.stockModel.getStockByCode(stockStr)

        if StockResult == None :
            return f"查無股票資訊:{stockStr}"

        # 查詢資料庫
        responseResult = self.stockModel.get_findbig(stockStr)

        if StockResult == None :
            return f"查無股票大股東資訊:{stockStr}"


        lastData = responseResult.iloc[1]

        #回覆訊息範本
        resultMessage = """
==個股大股東資訊查詢結果==
股票代號    {stockCode}
股票名稱    {stockName}
資料日期        {data1}
集保總張數              {data2}
總股東人數                {data3}
平均張數/人               {data4}
>400張大股東持有張數       {data5}
>400張大股東持有百分比        {data6}
>400張大股東人數              {data7}
400~600張人數               {data8}
600~800張人數               {data9}
800~1000張人數              {data10}
>1000張人數                {data11}
>1000張大股東持有百分比       {data12}
收盤價                  {data13}
        """
#正規式替換內容
        resultMessage = re.sub(r'{stockCode}',StockResult[1],resultMessage)
        resultMessage = re.sub(r'{stockName}',StockResult[2],resultMessage)
        resultMessage = re.sub(r'{data1}',lastData['資料日期'],resultMessage)
        resultMessage = re.sub(r'{data2}',lastData['集保總張數'],resultMessage)        
        resultMessage = re.sub(r'{data3}',lastData['總股東人數'],resultMessage)
        resultMessage = re.sub(r'{data4}',lastData['平均張數/人'],resultMessage)
        resultMessage = re.sub(r'{data5}',lastData['>400張大股東持有張數'],resultMessage)
        resultMessage = re.sub(r'{data6}',lastData['>400張大股東持有百分比'],resultMessage)
        resultMessage = re.sub(r'{data7}',lastData['>400張大股東人數'],resultMessage)
        resultMessage = re.sub(r'{data8}',lastData['400~600張人數'],resultMessage)        
        resultMessage = re.sub(r'{data9}',lastData['600~800張人數'],resultMessage)
        resultMessage = re.sub(r'{data10}',lastData['800~1000張人數'],resultMessage)
        resultMessage = re.sub(r'{data11}',lastData['>1000張人數'],resultMessage)
        resultMessage = re.sub(r'{data12}',lastData['>1000張大股東持有百分比'],resultMessage)
        resultMessage = re.sub(r'{data13}',lastData['收盤價'],resultMessage)

        return resultMessage