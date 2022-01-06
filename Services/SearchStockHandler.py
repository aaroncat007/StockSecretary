#!/usr/bin/python
# -*- coding:utf-8 -*-

from datetime import date
from numpy import datetime_as_string, round_
from Services.MessageHandler import MessageHandler
from Models.StockModel import StockModel
import re
import telepot
import time
from telepot.loop import MessageLoop
from PIL import Image
#from pprint import pprin
import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
token = "5042070567:AAHzhio9A3c9WF398wmzGbPgy0pj2q-_xPw"

bot = telegram.Bot(token=token)


TELEGRAM_BOT_TOKEN = '5042070567:AAHzhio9A3c9WF398wmzGbPgy0pj2q-_xPw'
TELEGRAM_CHAT_ID = '512226456'



bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)

bot.send_message(chat_id=TELEGRAM_CHAT_ID, text="沒有題目的高軟!!!")

#bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=open(, 'rb'))

# 查詢股票資訊
class SearchStockHandler(MessageHandler):

    COMMAND_HELP = "HELP"
    COMMAND_QUERY = "QUERY"
    COMMAND_GETNOW = "GETNOW"
    COMMAND_GETPE= "GETPE"
    COMMAND_GETK = "GETK"
    

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
            "取得k值資料"#(新增)
            stockStr = message.text
            response = self.QueryStock_PE(stockStr)
            return response
        elif  COMMAND == self.COMMAND_GETK:
            "取得k值資料"#(新增)
            stockStr = message.text
            response = self.QueryStock_K(stockStr)
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

        # 查詢資料庫
        queryResult = self.stockModel.getStockData_Now(stockStr)

        if queryResult == None :
            return f"查無股票資訊:{stockStr}"
        
        #回覆訊息範本
        resultMessage = """
股票及時:{stockprice}


"""
#正規式替換內容
        resultMessage = re.sub(r'{stockprice}',str(round(queryResult,2)),resultMessage)

        return resultMessage

    def QueryStock_PE(self,stockStr):
        """
        查詢股票資訊
        :param stockStr:股票代碼
        """
        # 進來的格式會是 /stock 股票代碼
        # 移除命令並去除空白
        stockStr = stockStr.replace('/PE','')
        stockStr = stockStr.strip()

        if stockStr == "":
            return f"請輸入股票代碼"

        # 查詢資料庫
        queryResult = self.stockModel.getStockData_Now(stockStr)

        if queryResult == None :
            return f"查無股票資訊:{stockStr}"
            
        #回覆訊息範本
        resultMessage = """
大股東:{Bigsh}
        """
#正規式替換內容
        resultMessage = re.sub(r'{Bigsh}',queryResult,resultMessage)
        return resultMessage



    def QueryStock_K(self,stockStr):
        """
        查詢股票資訊
        :param stockStr:股票代碼
        """
        # 進來的格式會是 /stock 股票代碼
        # 移除命令並去除空白
        stockStr = stockStr.replace('/K','')
        stockStr = stockStr.strip()
        
        if stockStr == "":
            return f"請輸入股票代碼"

        # 查詢資料庫
        data,path = self.stockModel.Get_todayK_line(stockStr)
        
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text="K線今日走勢圖")
        #bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=data)
        bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=open(path, 'rb'))
        
        if data == None :
            return f"查無股票資訊:{stockStr}"
        #回覆訊息範本
        resultMessage = """
大股東:{K_line}

        """
        #result = Image('./K line Jpg/{stockCode}.jpg')
        #return result

        
#正規式替換內容
        #resultMessage = re.sub(r'{K_line}',data,resultMessage)
        #resultMessage = re.sub(r'{K_line_p}',path,resultMessage)
        #return resultMessage

