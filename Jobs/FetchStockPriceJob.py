#!/usr/bin/python
# -*- coding:utf-8 -*-

import schedule  
import logging  
import functools  
import os  
import re  
import time  
from schedule import Job, CancelJob, IntervalError  
from datetime import datetime, timedelta  
from Models.StockMonitorModel import StockMonitorModel
from Models.StockModel import StockModel
from Models.UserModel import UserModel

class FetchStockPriceJob():
    "拉取股價資訊排程"

    def __init__(self):
        self.smModel = StockMonitorModel()
        self.stockModel = StockModel()
        self.userModel = UserModel()

    def run(self):
        print(f'Work Started at {datetime.now()}')