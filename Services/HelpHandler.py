#!/usr/bin/python
# -*- coding:utf-8 -*-

from os import name
from Services.MessageHandler import MessageHandler
from Models.UserModel import UserModel

# 幫助我
class HelpHandler(MessageHandler):

    def __init__(self):
        super().__init__()
        self.userModel = UserModel()

    def CheckUserExist(self,telegramID):
        "確認使用者是否註冊過"

        # 查詢資料庫內有無使用者
        userData = self.userModel.getUserByTelegramID(telegramID)

        if userData == None:
            return False
        else:
            return True

    def UpdateUserInfo(self,message):
        "更新使用者資訊"

        telegramID = message.from_user.id
        UserNickName = message.from_user.first_name + ' ' +message.from_user.last_name

        # 取得使用者資訊
        userData = self.userModel.getUserByTelegramID(telegramID)

        if userData != None:
            updateUserData = {
                'name':UserNickName,
                'id':userData[0]
            }
            updateUserReponse = self.userModel.UpdateUserName(updateUserData)
            if updateUserReponse > 0:
                return True, f"已更新 使用者 {UserNickName} 資訊"
            else:
                return False, f"更新失敗 使用者 {UserNickName} 資訊"
        return False, f"使用者 {UserNickName} 不存在"

    def RegisterUser(self,message):
        "註冊使用者"

        telegramID = message.from_user.id
        UserNickName = message.from_user.first_name + ' ' +message.from_user.last_name

        # 確認使用者是否註冊過
        isUserExist = self.CheckUserExist(telegramID)

        # 如果使用者不存在
        if isUserExist == False :

            # 建立使用者
            newUserdata = {
                'name': UserNickName,
                'telegramID': telegramID
            }
            addUserReponse = self.userModel.AddUser(newUserdata)
            if addUserReponse > 0 :
                return True, f"使用者 {UserNickName} 建立成功"
            else:
                return False, f"使用者 {UserNickName} 建立失敗"
        
        return False, f"使用者 {UserNickName} 已經存在"



    def getMessage(self,telegramID):
        "取得回應訊息"
        userData = self.userModel.getUserByTelegramID(telegramID)
        responseStr = "Hi " + userData[1] + ","
        responseStr += """\
I am Stock Secretary Bot.
很高興為您提供股市查詢服務!
以下說明訊息希望可以讓您更簡便的使用服務：
===============================
*查詢股票資訊: /stock 股票代碼 
*查詢大盤資訊: /TWStock
-股票數據-
    *查詢股票數據: /q 股票代碼
    *查詢日本益比: /pe 股票代碼
    *查詢K線圖: /k 股票代碼
    *查詢大股東資料: /big 股票代碼
-我的最愛-
    *新增我的喜好: /addfav 股票代碼
    *移除我的喜好: /delfav 股票代碼
    *列出我的喜好清單: /listfav
-股票監測-
    *新增股票監測: /addsm 股票代碼 監測類型 監測比較 值
    *移除股票監測: /delsm 監測代碼
    *停用股票監測: /dissm 監測代碼
    *啟用股票監測: /ensm 監測代碼
    *列出我的監測清單: /listsm
"""
        return responseStr