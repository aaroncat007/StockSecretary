#!/usr/bin/python
# -*- coding:utf-8 -*-


from Services.MessageHandler import MessageHandler

# 幫助我
class HelpHandler(MessageHandler):

    def __init__(self):
        super().__init__()

    def getMessage(self,userID):
        responseStr = "Hi " + super().db.getUser(userID) + ","
        responseStr += """\
I am Stock Secretary Bot.
目前我們還沒有提供服務!\
"""
        return responseStr