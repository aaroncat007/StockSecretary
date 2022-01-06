#!/usr/bin/python
# -*- coding:utf-8 -*-

import schedule  
import logging  
import telebot
import os  
import re  
import time  
from schedule import Job, CancelJob, IntervalError  
from datetime import datetime, timedelta  
from Models.StockMonitorModel import StockMonitorModel
from Models.StockModel import StockModel
from Models.UserModel import UserModel
from Models.StockMonitorModel import StockMonitorKind
from Models.StockMonitorModel import StockMonitorCompare
from Config.TelegramConfig import TelegramConfig

class FetchStockPriceJob():
    "拉取股價資訊排程"

    def __init__(self):
        self.smModel = StockMonitorModel()
        self.stockModel = StockModel()
        self.userModel = UserModel()

    def run(self):
        print(f'Work Started at {datetime.now()}')

        #取得目前監測的股票清單
        monitorList = self.smModel.getAllEnStockMonitor()

        # 股票代碼
        alertStockCodeList = []

        for i in monitorList:
            alertStockCodeList.append(i[2])

        alertStockCodeList = list(set(alertStockCodeList))

        # 取得股價
        if len(alertStockCodeList) < 2 :
            dataValues = self.stockModel.get_single_value(alertStockCodeList[0])
        else:
            dataValues = self.stockModel.get_multi_value(alertStockCodeList)

        # 找到是否滿足條件的
        for monitor in monitorList:
            # 是否觸發警報
            isAlert = False

            # 警報訊息
            alertMessage = ""
            
            userID = monitor[1]
            stockCode = monitor[2]
            triggerKind = monitor[3]
            triggerCompare = monitor[4]
            triggerValue = float(monitor[5])

            #取出指定股票的值
            targetStock = dataValues[dataValues['股票代碼']==stockCode]
            
            #若找不到 跳過
            if len(targetStock) <= 0 :
                continue

            #比對條件
            if triggerKind == StockMonitorKind.closing_price:
                realValue = targetStock['現價'][0]
                if triggerCompare == StockMonitorCompare.greater_than:
                    if realValue >= triggerValue:
                        isAlert = True
                elif triggerCompare == StockMonitorCompare.less_than:
                    if realValue <= triggerValue:
                        isAlert = True
                if isAlert:
                    alertMessage = self.createAlertMessage(stockCode,triggerKind,triggerCompare,triggerValue,realValue)
            elif triggerKind == StockMonitorKind.rise_fall_price:
                realValue = targetStock['價差'][0]
                if triggerCompare == StockMonitorCompare.greater_than:
                    if realValue >= triggerValue:
                        isAlert = True
                elif triggerCompare == StockMonitorCompare.less_than:
                    if realValue <= triggerValue:
                        isAlert = True
                if isAlert:
                    alertMessage = self.createAlertMessage(stockCode,triggerKind,triggerCompare,triggerValue,realValue)
            elif triggerKind == StockMonitorKind.rise_fall_rate:
                realValue = targetStock['漲跌幅'][0]
                if triggerCompare == StockMonitorCompare.greater_than:
                    if realValue >= triggerValue:
                        isAlert = True
                elif triggerCompare == StockMonitorCompare.less_than:
                    if realValue <= triggerValue:
                        isAlert = True
                if isAlert:
                    alertMessage = self.createAlertMessage(stockCode,triggerKind,triggerCompare,triggerValue,realValue)
            elif triggerKind == StockMonitorKind.trading_volume:
                realValue = targetStock['總量'][0]
                if triggerCompare == StockMonitorCompare.greater_than:
                    if realValue >= triggerValue:
                        isAlert = True
                elif triggerCompare == StockMonitorCompare.less_than:
                    if realValue <= triggerValue:
                        isAlert = True
                if isAlert:
                    alertMessage = self.createAlertMessage(stockCode,triggerKind,triggerCompare,triggerValue,realValue)
            elif triggerKind == StockMonitorKind.single_volume:
                realValue = targetStock['單量'][0]
                if triggerCompare == StockMonitorCompare.greater_than:
                    if realValue >= triggerValue:
                        isAlert = True
                elif triggerCompare == StockMonitorCompare.less_than:
                    if realValue <= triggerValue:
                        isAlert = True
                if isAlert:
                    alertMessage = self.createAlertMessage(stockCode,triggerKind,triggerCompare,triggerValue,realValue)
        if isAlert:
            self.NotifyUser(userID,alertMessage)

        print(f'Work Ended at {datetime.now()}')

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


    def createAlertMessage(self,stockCode,triggerKind,triggerCompare,triggerValue,realValue):
        """
        建立警示訊息
        """
        response = ""

        triggerCompareStr = ""
        if triggerCompare == StockMonitorCompare.greater_than:
            triggerCompareStr = ">="
        elif triggerCompare == StockMonitorCompare.less_than:
            triggerCompareStr = "<="

        stockData = self.stockModel.getStockByCode(stockCode)

        response += f"==觸發通知==\n"
        response += f"股票代號:{stockData[1]} \n"
        response += f"股票名稱:{stockData[2]} \n"
        response += f"觸發條件: 當 {triggerKind} {triggerCompareStr} {triggerValue} 時 \n"
        response += f"當前{triggerKind} = {realValue} \n"
        
        return response


