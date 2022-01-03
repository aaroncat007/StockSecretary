#!/usr/bin/python
# -*- coding:utf-8 -*-

from Repository.SQLiteRepository import SQLiteRepository
from Models.dbModel import dbModel
from datetime import datetime
import yahoo_fin.stock_info as si
import yfinance as yf

class StockMarketModel(dbModel):
    "大盤指數模型"

    TABLENAME = 'stockMarket'

    def __init__(self):
        # 取得資料倉儲
        self.repo = SQLiteRepository()
        self.initTable()

    #取得台股大盤資訊
    def getTWStock(self):
        id='^TWII'
        responseStr = ""
        toclos=float(yf.download(id,
                    period='1d',
                    interval='5m').iloc[-1:]['Close'])
        if int(datetime.now().strftime('%H'))>13:
            yes=si.get_data(id).iloc[-2:-1]
        elif int(datetime.now().strftime('%H'))<9:
            yes=si.get_data(id).iloc[-2:-1]
        else:
            yes=si.get_data(id).iloc[-1:]
        yeclos=float(yes['close'])
        yesop=float(yes['open']) 
        yeshg=float(yes['high']) 
        yeslo=float(yes['low']) 
        yesvalue=int(yes['volume']) 
        responseStr +=(f'大盤情形 \n')
        if toclos>yeclos:
            responseStr +=(f'現價{round(toclos,2)} ▲ {toclos-yeclos}, {round((toclos/yeclos-1)*100,2)}% \n')
            responseStr +=(f'昨日開盤    {round(yesop,2)} \n')
            responseStr +=(f'昨日收盤    {round(yeclos,2)} \n')
            responseStr +=(f'昨日最高    {round(yeshg,2)} \n')
            responseStr +=(f'昨日最低    {round(yeslo,2)} \n')
            responseStr +=(f'昨日成交量    {yesvalue} 張 \n')

        elif toclos==yeclos:
            responseStr +=(f'現價{round(toclos,2)} ● {toclos-yeclos}, {round((toclos/yeclos-1)*100,2)}% \n')
            responseStr +=(f'昨日開盤    {round(yesop,2)} \n')
            responseStr +=(f'昨日收盤    {round(yeclos,2)} \n')
            responseStr +=(f'昨日最高    {round(yeshg,2)} \n')
            responseStr +=(f'昨日最低    {round(yeslo,2)} \n')
            responseStr +=(f'昨日成交量    {yesvalue} 張 \n')

        else:
            responseStr +=(f'{toclos} ▼ {yeclos-toclos}, {round((yeclos/toclos-1)*100,2)}% \n')
            responseStr +=(f'昨日開盤    {round(yesop,2)} \n')
            responseStr +=(f'昨日收盤    {round(yeclos,2)} \n')
            responseStr +=(f'昨日最高    {round(yeshg,2)} \n')
            responseStr +=(f'昨日最低    {round(yeslo,2)} \n')
            responseStr +=(f'昨日成交量  {yesvalue} 張 \n')

        return responseStr


    def initTable(self):
        """
        初始化資料表
        """
        conn = self.repo.getConn()
        c = conn.cursor()
        pass