#!/usr/bin/python
# -*- coding:utf-8 -*-

import pandas as pd
import schedule  
import logging  
import telebot
import os  
import re  
import time  
from schedule import Job, CancelJob, IntervalError  
from datetime import datetime, timedelta
from Models.FavouriteModel import FavouriteModel  
from Models.StockMonitorModel import StockMonitorModel
from Models.StockModel import StockModel
from Models.UserModel import UserModel
from Models.StockMonitorModel import StockMonitorKind
from Models.StockMonitorModel import StockMonitorCompare
from Config.TelegramConfig import TelegramConfig

class AhdJob():
    "盤後資訊排程"

    def __init__(self):
        self.stockModel = StockModel()
        self.userModel = UserModel()
        self.favModel = FavouriteModel()

    def run(self):

        #取得使用者清單
        allUserData = self.userModel.getAllUser()

        for user in allUserData:

            userID = user[0]

            #拿出喜愛的模型
            userFavList = self.favModel.listUserStock(userID)

            # 股票代碼
            alertStockCodeList = []

            for i in userFavList:
                alertStockCodeList.append(i[2])

            alertStockCodeList = list(set(alertStockCodeList))

            # 取得股價
            if len(alertStockCodeList) < 2 :
                dataValues = self.stockModel.get_single_value(alertStockCodeList[0])
            else:
                dataValues = self.stockModel.get_multi_value(alertStockCodeList)

            responseMsg = f"Hi {user[1]},這是今天的盤後資料\n"
            for index in dataValues['股票代碼']:
                valueObj = dataValues[dataValues['股票代碼'] == index]
                msg = self.createMessage(valueObj)
                responseMsg += f"{msg} \n---\n"

            #通知使用者
            self.NotifyUser(userID,responseMsg)

    def NotifyUser(self,userID,message):
        """
        通知使用者
        """

        userData = self.userModel.getUser(userID)
        if userData == None:
            return "找不到使用者"

        chatID = userData[2]
        bot = telebot.TeleBot(TelegramConfig.API_TOKEN)

        #通知
        bot.send_message(chatID,message)

    def createMessage(self,valueObj):
        "建立通知訊息"
        stockCode = valueObj["股票代碼"][0]
        stockData = self.stockModel.getStockByCode(stockCode)
        stockName = stockData[2]

        #整理格式
        SpStr = round(valueObj["價差"][0],2)
        if SpStr < 0 :
            SpStr = f" ▼ {SpStr}"
        elif SpStr > 0:
            SpStr = f" ▲ {SpStr}"
        else:
            SpStr = f" ● {SpStr}"      

        AmpStr = round(valueObj["漲跌幅"][0],2)
        if AmpStr < 0 :
            AmpStr = f" ▼ {AmpStr}"
        elif AmpStr > 0:
            AmpStr = f" ▲ {AmpStr}"
        else:
            AmpStr = f" ● {AmpStr}"             


        resultMessage = """
股票代號    {stockCode}
股票名稱    {stockName}
收盤價格    {stockprice}
價差        {價差}
漲跌幅      {漲跌幅}
單量        {單量}
總量        {總量}
"""

#正規式替換內容
        resultMessage = re.sub(r'{stockCode}',stockCode,resultMessage)
        resultMessage = re.sub(r'{stockName}',stockName,resultMessage)
        resultMessage = re.sub(r'{stockprice}',str(round(valueObj,2)),resultMessage)
        resultMessage = re.sub(r'{價差}',SpStr,resultMessage)
        resultMessage = re.sub(r'{漲跌幅}',AmpStr,resultMessage)
        resultMessage = re.sub(r'{單量}',str(valueObj["單量"][0]),resultMessage)
        resultMessage = re.sub(r'{總量}',str(valueObj["總量"][0]),resultMessage)
