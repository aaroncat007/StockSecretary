#!/usr/bin/python
# -*- coding:utf-8 -*-

import re
from os import name
from Services.MessageHandler import MessageHandler
from Models.StockMonitorModel import StockMonitorModel,StockMonitorKind,StockMonitorCompare
from Models.UserModel import UserModel
from Models.StockModel import StockModel

class StockMonitorHandler(MessageHandler):
    "我的監測管理服務"

    COMMAND_GET_LIST = "GET_LIST"
    COMMAND_ADD_MONITOR = "ADD_STOCK"
    COMMAND_REMOVE_MONITOR = "REMOVE_STOCK"
    COMMAND_DISABLE_MONITOR = "DISABLE_MONITOR"
    COMMAND_ENABLE_MONITOR = "ENABLE_MONITOR"
    COMMAND_HELP = "HELP"
    
    def __init__(self):
        super().__init__()
        self.smModel = StockMonitorModel() #股票監測模型
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
            "取得股票監測清單"
            response = self.GET_LIST(userID)
            return response

        elif COMMAND == self.COMMAND_ADD_MONITOR:
            "新增股票監測"
            # 進來的格式會是 /addsm 股票代碼 監測類型 監測比較 值
            # 移除命令並去除空白
            smStr = message.text

            smStrArray = smStr.split()

            if len(smStrArray) != 5:
                return f"輸入格式不正確!請參閱說明:\n {self.helpMessage}"

            response = self.ADD_STOCK(userID,smStrArray)
            return response

        elif COMMAND == self.COMMAND_REMOVE_MONITOR:
            "移除股票監測"
            # 進來的格式會是 /delsm 股票代碼
            # 移除命令並去除空白
            smStr = message.text         
            smStrArray = smStr.split()

            if len(smStrArray) != 2:
                return f"輸入格式不正確!請參閱說明:\n {self.helpMessage}"

            response = self.REMOVE_STOCK(userID,smStrArray)
            return response

        elif COMMAND == self.COMMAND_ENABLE_MONITOR:
            "啟用股票監測"
            # 進來的格式會是 /ensm 股票代碼
            # 移除命令並去除空白
            smStr = message.text         
            smStrArray = smStr.split()

            if len(smStrArray) != 2:
                return f"輸入格式不正確!請參閱說明:\n {self.helpMessage}"

            response = self.ENABLE_STOCK(userID,smStrArray)
            return response

        elif COMMAND == self.COMMAND_DISABLE_MONITOR:
            "停用股票監測"
            # 進來的格式會是 /dissm 股票代碼
            # 移除命令並去除空白
            smStr = message.text         
            smStrArray = smStr.split()

            if len(smStrArray) != 2:
                return f"輸入格式不正確!請參閱說明:\n {self.helpMessage}"

            response = self.DISABLE_STOCK(userID,smStrArray)
            return response 

        elif COMMAND == self.COMMAND_HELP:
            "取得說明"
            response = self.helpMessage()
            return response

        else:
            return f"未定義指令:{COMMAND}"


    # 取得我的監測清單
    def GET_LIST(self,userID):
        usersmList = self.smModel.listUserStockMonitor(userID)
        response = """
目前您的監測名單如下：    
共 {count} 項    
=====================
"""
        count = 1
        for usersm in usersmList:
            
            # 引入範本
            response += self.template(usersm)

            #序列增加
            count+=1

        response += """
=====================
"""

        #正規式替換內容
        response = re.sub(r'{count}',str(count-1),response)

        return response
    
    # 新增我的喜愛清單
    # /addsm 股票代碼 監測類型 監測比較 值
    def ADD_STOCK(self,userID,smStrArray):

        _stockCode = smStrArray[1]

        #確認股票存在
        _stock = self.stockModel.getStockByCode(_stockCode)
        if _stock == None:
            return f"股票代號 [{_stockCode}] 不存在"

        #判定監測類型存在
        _smKind = ""
        if smStrArray[2] == "成交價":
            _smKind = StockMonitorKind.closing_price
        elif smStrArray[2] == "漲跌價":
            _smKind = StockMonitorKind.rise_fall_price
        elif smStrArray[2] == "漲跌幅度":
            _smKind = StockMonitorKind.rise_fall_rate
        elif smStrArray[2] == "成交量":
            _smKind = StockMonitorKind.trading_volume
        elif smStrArray[2] == "單量":
            _smKind = StockMonitorKind.single_volume
        else:
            return f"監測類型錯誤"

        #判定監測比較方式存在
        _smCompare = ""
        if smStrArray[3] == "gt":
            _smCompare = StockMonitorCompare.greater_than
        elif smStrArray[3] == "lt":
            _smCompare = StockMonitorCompare.less_than
        else:
            return f"監測比較方式錯誤"

        #確定股票尚未存在我的喜愛清單內
        userSMArray = self.smModel.getUserStockByStock(userID,_stockCode)
        if len(userSMArray) != 0:
            for userSM in userSMArray:
                if userSM[3] == _smKind \
                & userSM[4] ==_smCompare \
                & userSM[5] == smStrArray[4]:
                    return f"股票代號 [{_stockCode}] 已經存在監測清單內"           

        #寫入資料庫
        isSuccess = self.smModel.addUserStockMonitor(userID,_stockCode,_smKind,_smCompare,smStrArray[4])
        if isSuccess == True:
            return f"股票代號 [{_stockCode} - {_stock[2]}] 監測新增成功"
        else :
            return f"股票代號 [{_stockCode} - {_stock[2]}] 監測新增失敗"

    # 移除我的監測清單
    def REMOVE_STOCK(self,userID,smStrArray):

        smID = smStrArray[1]

        #確定股票存在我的監測清單內
        smData = self.smModel.getUserStockMonitorByID(smID)
        if smData == None:
            return f"監測代號 [{smID}] 不存在清單內"

        #確定這條監測屬於這使用者
        isown = smData[1] == userID
        if isown == False:
            return f"監測代號 [{smID}] 不存在清單內"      

        #更新資料庫
        isSuccess = self.smModel.removeUserStockMonitorByID(smID)
        if isSuccess == True:
            return f"監測代號 [{smID}] 已成功移除我的監測清單"
        else :
            return f"監測代號 [{smID}] 移除我的監測失敗"       

    # 啟用我的監測
    def ENABLE_STOCK(self,userID,smStrArray):

        smID = smStrArray[1]

        #確定股票存在我的監測清單內
        smData = self.smModel.getUserStockMonitorByID(smID)
        if smData == None:
            return f"監測代號 [{smID}] 不存在清單內"

        #確定這條監測屬於這使用者
        isown = smData[1] == userID
        if isown == False:
            return f"監測代號 [{smID}] 不存在清單內"      

        #更新資料庫
        isSuccess = self.smModel.enableStockMonitor(smID)
        if isSuccess == True:
            return f"監測代號 [{smID}] 已成功啟用我的監測"
        else :
            return f"監測代號 [{smID}] 啟用我的監測失敗"   

    # 停用我的監測
    def DISABLE_STOCK(self,userID,smStrArray):

        smID = smStrArray[1]

        #確定股票存在我的監測清單內
        smData = self.smModel.getUserStockMonitorByID(smID)
        if smData == None:
            return f"監測代號 [{smID}] 不存在清單內"

        #確定這條監測屬於這使用者
        isown = smData[1] == userID
        if isown == False:
            return f"監測代號 [{smID}] 不存在清單內"      

        #更新資料庫
        isSuccess = self.smModel.disableStockMonitor(smID)
        if isSuccess == True:
            return f"監測代號 [{smID}] 已成功停用我的監測"
        else :
            return f"監測代號 [{smID}] 停用我的監測失敗"   

    def template(self,StockMonitor):
        "輸出範本"
        stockCode = StockMonitor[2]
        #查詢股票資料
        _stock = self.stockModel.getStockByCode(stockCode)
        if _stock == None:
            return f"股票代號 [{stockCode}] 不存在"

        #狀態
        _smStatus = ""
        if StockMonitor[6] == 1:
            _smStatus="啟用"
        else:
            _smStatus="未啟用"

        #判斷類型
        _smKindStr = ""
        if StockMonitor[3] == StockMonitorKind.closing_price:
            _smKindStr = "成交價"
        elif StockMonitor[3] == StockMonitorKind.rise_fall_price:
            _smKindStr = "漲跌價"
        elif StockMonitor[3] == StockMonitorKind.rise_fall_rate:
            _smKindStr = "漲跌幅度"
        elif StockMonitor[3] == StockMonitorKind.trading_volume:
            _smKindStr = "成交量"
        elif StockMonitor[3] == StockMonitorKind.single_volume:
            _smKindStr = "單量"
        else:
            _smKindStr = f"監測類型錯誤"

        #判斷條件
        _smCompare = ""
        if StockMonitor[4] == "gt":
            _smCompare = ">="
        elif StockMonitor[4] == "lt":
            _smCompare = "<="
        else:
            _smCompare = ""

        response = ""
        response += f"監測代碼:{StockMonitor[0]}\n"
        response += f"監測股票:{_stock[1]}-{_stock[2]} \n"
        response += f"狀態:{_smStatus}\n"
        response += f"監測條件:\n"
        response += f"當 {_smKindStr} {_smCompare} {StockMonitor[5]} 時通知 \n"
        response += f"---\n"

        return response


    def helpMessage(self):
        "使用說明"
        return """
*新增股票監測: /addsm 股票代碼 監測類型 監測比較 值
[監測類型]有以下幾種:
1. 成交價
2. 漲跌價
3. 漲跌幅度
4. 成交量
5. 單量

[監測比較方式]
1.大於: gt
2.小於: lt

範例: 當希望東泥成交價大於等於20元時收到通知
/addsm 1110 成交價 gt 20

*移除股票監測: /delsm 監測代碼
*停用股票監測: /dissm 監測代碼
*啟用股票監測: /ensm 監測代碼
*列出我的監測清單: /listsm
"""