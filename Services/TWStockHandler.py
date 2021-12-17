#!/usr/bin/python
# -*- coding:utf-8 -*-

from Services.MessageHandler import MessageHandler

# 大盤指數
class TWStockHandler(MessageHandler):

    def __init__(self):
        super().__init__()

    def getMessage(self):
        return super().db.getTWStock()