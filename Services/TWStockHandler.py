#!/usr/bin/python
# -*- coding:utf-8 -*-

from Services.MessageHandler import MessageHandler
from Models.StockMarketModel import StockMarketModel

# 大盤指數
class TWStockHandler(MessageHandler):

    def __init__(self):
        super().__init__()
        self.smModel = StockMarketModel()

    def getMessage(self):
        "取得回應訊息"
        response = self.smModel.getTWStock()
        return response