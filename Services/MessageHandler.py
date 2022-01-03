#!/usr/bin/python
# -*- coding:utf-8 -*-

from abc import ABCMeta, abstractmethod

from Models.CSVModel import CSVModel
from Models.dbModel import dbModel

# 訊息處理服務
class MessageHandler(metaclass=ABCMeta):
    
    #資料庫模型
    db = CSVModel()

    def __init__(self):
        pass

    @abstractmethod
    def getMessage(self):
        "取得回應訊息"
        pass
    
