#!/usr/bin/python
# -*- coding:utf-8 -*-

import re
from os import name
from Services.MessageHandler import MessageHandler
from Models.FavouriteModel import FavouriteModel
from Models.UserModel import UserModel
from Models.StockModel import StockModel

class FavouriteHandler(MessageHandler):
    "我的喜愛管理服務"

    COMMAND_GET_LIST = "GET_LIST"
    COMMAND_ADD_STOCK = "ADD_STOCK"
    COMMAND_REMOVE_STOCK = "REMOVE_STOCK"
    COMMAND_HELP = "HELP"
    
    def __init__(self):
        super().__init__()
        self.favModel = FavouriteModel() #我的喜愛模型
        self.userModel = UserModel()     #用戶模型
        self.stockModel = StockModel()   #股票模型

    def getMessage(self,message,handler="GET_LIST"):
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

        # 查詢資料庫內有無使用者
        userData = self.userModel.getUserByTelegramID(telegramID)
        if userData == None:
            return "系統中不存在您的帳號資訊"
        # 使用者ID
        userID = userData[0]

        # 指令判斷
        if COMMAND == self.COMMAND_GET_LIST:
            "取得清單"
            response = self.GET_LIST(userID)
            return response

        elif COMMAND == self.COMMAND_ADD_STOCK:
            "新增股票"
            # 進來的格式會是 /addstock 股票代碼
            # 移除命令並去除空白
            stockStr = message.text
            stockStr = stockStr.replace('/addfav','')
            stockStr = stockStr.strip()

            response = self.ADD_STOCK(userID,stockStr)
            return response
            
           
            


        elif COMMAND == self.COMMAND_REMOVE_STOCK:
            "移除股票"
            # 進來的格式會是 /delstock 股票代碼
            # 移除命令並去除空白
            stockStr = message.text
            stockStr = stockStr.replace('/delfav','')
            stockStr = stockStr.strip()

            response = self.REMOVE_STOCK(userID,stockStr)
            return response

        elif  COMMAND == self.COMMAND_HELP:
            "取得說明"
            response = self.helpMessage()
            return response
        
        else:
            return f"未定義指令:{COMMAND}"

    # 取得我的喜愛清單
    def GET_LIST(self,userID):
        userFavList = self.favModel.listUserStock(userID)
        response = """
目前您的喜愛名單如下：    
共 {count} 項    
=====================
"""
        count = 1
        for userFav in userFavList:
            
            # 查詢股票資訊
            _stockCode = userFav[2]
            _stock = self.stockModel.getStockByCode(_stockCode)

            # 股票名稱
            _stockName = _stock[2]
            response += f"{count}: {_stockCode} - {_stockName} \r\n"

            #序列增加
            count+=1

        response += """
=====================
"""

        #正規式替換內容
        response = re.sub(r'{count}',str(count-1),response)

        return response
    
    # 新增我的喜愛清單
    def ADD_STOCK(self,userID,stockCode):

        #確認股票存在
        _stock = self.stockModel.getStockByCode(stockCode)
        if _stock == None:
            return f"股票代號 [{stockCode}] 不存在"

        #確定股票尚未存在我的喜愛清單內
        isFavExist = self.favModel.getUserStock(userID,stockCode)
        if isFavExist != None:
            return f"股票代號 [{stockCode}] 已經存在清單內"

        #寫入資料庫
        isSuccess = self.favModel.addUserStock(userID,stockCode)
        if isSuccess == True:
            return f"股票代號 [{stockCode} - {_stock[2]}] 新增成功"
        else :
            return f"股票代號 [{stockCode} - {_stock[2]}] 新增失敗"

    # 移除我的喜愛清單
    def REMOVE_STOCK(self,userID,stockCode):

        #確定股票存在我的喜愛清單內
        isFavExist = self.favModel.getUserStock(userID,stockCode)
        if isFavExist == None:
            return f"股票代號 [{stockCode}] 不存在清單內"

        #查詢股票資料
        _stock = self.stockModel.getStockByCode(stockCode)
        if _stock == None:
            return f"股票代號 [{stockCode}] 不存在"

        #更新資料庫
        isSuccess = self.favModel.removeUserStock(userID,stockCode)
        if isSuccess == True:
            return f"股票代號 [{stockCode} - {_stock[2]}] 已成功移除我的喜愛"
        else :
            return f"股票代號 [{stockCode} - {_stock[2]}] 移除我的喜愛失敗"      
        
        def helpMessage(self):
         "使用說明"
        return """
*新增我的喜好: /addfav 股票代碼
*移除我的喜好: /delfav 股票代碼
*列出我的喜好清單: /listfav
"""


    
        def helpMessage(self):
         "使用說明"
        return """
*新增我的喜好: /addfav 股票代碼
*移除我的喜好: /delfav 股票代碼
*列出我的喜好清單: /listfav
"""
        
