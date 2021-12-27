#!/usr/bin/python
# -*- coding:utf-8 -*-

import telebot

from Services.HelpHandler import HelpHandler
from Services.TWStockHandler import TWStockHandler
from Services.SearchStockHandler import SearchStockHandler
from Services.FavouriteHandler import FavouriteHandler

API_TOKEN = '5042070567:AAHzhio9A3c9WF398wmzGbPgy0pj2q-_xPw'

bot = telebot.TeleBot(API_TOKEN)

# 初始提示訊息
def start_executor(message):
    helpHandler = HelpHandler()

    #確認使用者是否存在
    isUserExist = HelpHandler.CheckUserExist(message.from_user.id)
    if isUserExist:
        #若存在 更新使用者資訊
        helpHandler.UpdateUserInfo(message)
    else:
        #若不存在 新增使用者
        helpHandler.RegisterUser(message)
    
    bot.send_message(message.chat.id,  helpHandler.getMessage(message.from_user.id))

# 查詢股票基本資訊
def search_stock(message):
    searchStockHandler = SearchStockHandler()
    bot.reply_to(message,searchStockHandler.getMessage(message.text))

# 查詢大盤資訊
def print_TWStock(message):
    twStockHandler = TWStockHandler()
    bot.reply_to(message,twStockHandler.getMessage())

# 新增我的最愛
def add_myfavourite(message):
    favouriteHandler = FavouriteHandler()
    bot.reply_to(message,favouriteHandler.getMessage(message,favouriteHandler.COMMAND_ADD_STOCK))
    pass

# 移除我的最愛
def remove_myfavourite(message):
    favouriteHandler = FavouriteHandler()
    bot.reply_to(message,favouriteHandler.getMessage(message,favouriteHandler.COMMAND_REMOVE_STOCK))
    pass

# 列出我的最愛清單
def list_myfavourite(message):
    favouriteHandler = FavouriteHandler()
    bot.reply_to(message,favouriteHandler.getMessage(message,favouriteHandler.COMMAND_GET_LIST))
    pass

# 註冊指令事件
bot.register_message_handler(start_executor, commands=['start','help'])
bot.register_message_handler(search_stock,commands=['stock'])
bot.register_message_handler(print_TWStock,commands=['TWStock'])
bot.register_message_handler(add_myfavourite,commands=['addstock'])
bot.register_message_handler(remove_myfavourite,commands=['delstock'])
bot.register_message_handler(list_myfavourite,commands=['liststock'])

# 註冊一般文字事件
# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)


bot.infinity_polling()