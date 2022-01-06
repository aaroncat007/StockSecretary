#!/usr/bin/python
# -*- coding:utf-8 -*-

import telebot
import schedule
import threading
import time
from telebot import types

from Services.HelpHandler import HelpHandler
from Services.TWStockHandler import TWStockHandler
from Services.SearchStockHandler import SearchStockHandler
from Services.FavouriteHandler import FavouriteHandler
from Services.StockMonitorHandler import StockMonitorHandler
from Config.TelegramConfig import TelegramConfig
from Jobs.FetchStockPriceJob import FetchStockPriceJob
from Jobs.AhdJob import AhdJob

bot = telebot.TeleBot(TelegramConfig.API_TOKEN)

# 註冊排程
# 參考
# https://schedule.readthedocs.io/en/stable/examples.html

#每30秒執行一次
fspJob = FetchStockPriceJob()
schedule.every(30).seconds.do(fspJob.run)

#開盤日四點執行一次
schedule.every().monday.at("16:00").do(AhdJob().run)
schedule.every().tuesday.at("16:00").do(AhdJob().run)
schedule.every().wednesday.at("16:00").do(AhdJob().run)
schedule.every().thursday.at("16:00").do(AhdJob().run)
schedule.every().friday.at("16:00").do(AhdJob().run)

def run_continuously(interval=1):
    """Continuously run, while executing pending jobs at each
    elapsed time interval.
    @return cease_continuous_run: threading. Event which can
    be set to cease continuous run. Please note that it is
    *intended behavior that run_continuously() does not run
    missed jobs*. For example, if you've registered a job that
    should run every minute and you set a continuous run
    interval of one hour then your job won't be run 60 times
    at each interval but only once.
    """
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run

# Start the background thread
stop_run_continuously = run_continuously()

# 註冊 Markup
markup = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=False)
itembtn1 = types.KeyboardButton('/helpstock')
itembtn2 = types.KeyboardButton('/helpfav')
itembtn3 = types.KeyboardButton('/helpsm')
itembtn4 = types.KeyboardButton('/addfav')
itembtn5 = types.KeyboardButton('/delfav')
itembtn6 = types.KeyboardButton('/listfav')
#按鈕
markup.row(itembtn1, itembtn2, itembtn3)
markup.row(itembtn4, itembtn5, itembtn6)
# 初始提示訊息
def start_executor(message):
    helpHandler = HelpHandler()

    #確認使用者是否存在
    isUserExist = helpHandler.CheckUserExist(message.from_user.id)
    if isUserExist:
        #若存在 更新使用者資訊
        helpHandler.UpdateUserInfo(message)
    else:
        #若不存在 新增使用者
        helpHandler.RegisterUser(message)
    
    bot.send_message(message.chat.id,  helpHandler.getMessage(message.from_user.id), reply_markup=markup)

# 查詢股票基本資訊
def search_stock(message):
    searchStockHandler = SearchStockHandler()
    bot.reply_to(message,searchStockHandler.getMessage(message))

# 查詢股票基本資訊
def search_stock(message):
    searchStockHandler = SearchStockHandler()
    bot.reply_to(message,searchStockHandler.getMessage(message))


# 說明股票基本資訊
def help_search_stock(message):
    searchStockHandler = SearchStockHandler()
    bot.reply_to(message,searchStockHandler.getMessage(message,searchStockHandler.COMMAND_HELP))

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

# 說明我的喜愛
def help_myfavourite(message):
    favouriteHandler = FavouriteHandler()
    bot.reply_to(message,favouriteHandler.getMessage(message,favouriteHandler.COMMAND_HELP))
    pass

# 列出我的監測清單
def list_myMonitor(message):
    smHandler = StockMonitorHandler()
    bot.reply_to(message,smHandler.getMessage(message,smHandler.COMMAND_GET_LIST))
    pass

# 新增我的監測清單
def add_myMonitor(message):
    smHandler = StockMonitorHandler()
    bot.reply_to(message,smHandler.getMessage(message,smHandler.COMMAND_ADD_MONITOR))
    pass

# 移除我的監測清單
def remove_myMonitor(message):
    smHandler = StockMonitorHandler()
    bot.reply_to(message,smHandler.getMessage(message,smHandler.COMMAND_REMOVE_MONITOR))
    pass

# 停用我的監測
def disable_myMonitor(message):
    smHandler = StockMonitorHandler()
    bot.reply_to(message,smHandler.getMessage(message,smHandler.COMMAND_DISABLE_MONITOR))
    pass

# 啟用我的監測
def enable_myMonitor(message):
    smHandler = StockMonitorHandler()
    bot.reply_to(message,smHandler.getMessage(message,smHandler.COMMAND_ENABLE_MONITOR))
    pass

# 說明我的監測
def help_myMonitor(message):
    smHandler = StockMonitorHandler()
    bot.reply_to(message,smHandler.getMessage(message,smHandler.COMMAND_HELP))
    pass

#及時股票 (新增)
def query_stock_now(message):
    searchStockHandler = SearchStockHandler()
    bot.reply_to(message,searchStockHandler.getMessage(message,searchStockHandler.COMMAND_GETNOW))
    pass

#日本益比資料(新增)
def query_stock_PE(message):
    searchStockHandler = SearchStockHandler()
    bot.reply_to(message,searchStockHandler.getMessage(message,searchStockHandler.COMMAND_GETPE))

#k值股票 (新增)
def query_stock_K(message):
    searchStockHandler = SearchStockHandler()
    response = searchStockHandler.getMessage(message,searchStockHandler.COMMAND_GETK)

    #如果是圖片 則使用send_photo回傳
    if response[0] == "img":
        bot.send_photo(message.chat.id,response[1])
    else:
        bot.reply_to(message,response[1])
    pass

#大股東資料
def query_stock_big(message):
    searchStockHandler = SearchStockHandler()
    bot.reply_to(message,searchStockHandler.getMessage(message,searchStockHandler.COMMAND_GETBIG))


# 註冊指令事件
# 一般查詢
bot.register_message_handler(start_executor, commands=['start','help'])
bot.register_message_handler(search_stock,commands=['stock'])
bot.register_message_handler(help_search_stock, commands=['helpstock'])
bot.register_message_handler(print_TWStock,commands=['TWStock'])
# 我的最愛
bot.register_message_handler(add_myfavourite,commands=['addfav'])
bot.register_message_handler(remove_myfavourite,commands=['delfav'])
bot.register_message_handler(list_myfavourite,commands=['listfav'])
bot.register_message_handler(help_myfavourite,commands=['helpfav'])
# 我的監測
bot.register_message_handler(help_myMonitor,commands=['helpsm'])
bot.register_message_handler(list_myMonitor,commands=['listsm'])
bot.register_message_handler(add_myMonitor,commands=['addsm'])
bot.register_message_handler(remove_myMonitor,commands=['delsm'])
bot.register_message_handler(enable_myMonitor,commands=['ensm'])
bot.register_message_handler(disable_myMonitor,commands=['dissm'])
# 股票數據查詢
bot.register_message_handler(query_stock_now,commands=['q'])
bot.register_message_handler(query_stock_PE,commands=['pe'])
bot.register_message_handler(query_stock_K,commands=['k'])
bot.register_message_handler(query_stock_big,commands=['big'])

#
# 註冊一般文字事件
# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)

bot.infinity_polling()

try:
    while 1:
        time.sleep(.1)
except KeyboardInterrupt:
    print("attempting to close threads.")
    # Stop the background thread
    stop_run_continuously.set()