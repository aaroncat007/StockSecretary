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
目前我們還沒有提供服務!\
"""
        return responseStr