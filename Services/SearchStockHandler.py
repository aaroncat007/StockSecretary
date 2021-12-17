#!/usr/bin/python
# -*- coding:utf-8 -*-

from Services.MessageHandler import MessageHandler

# 查詢股票資訊
class SearchStockHandler(MessageHandler):

    def __init__(self):
        super().__init__()

    def getMessage(self,stockStr):
        # 進來的格式會是 /stock 股票代碼
        # 移除命令並去除空白

        stockStr = stockStr.replace('/stock','')
        stockStr = stockStr.strip()

        return super().db.getStock(stockStr)