#!/usr/bin/python
# -*- coding:utf-8 -*-

import requests
import pandas as pd
from Models.StockModel import StockModel

class StockSeed:
    "提供初始化股票資料"

    def __init__(self):
        pass

    def run(self):
        #拉上市股票
        url = f"https://isin.twse.com.tw/isin/class_main.jsp?owncode=&stockname=&isincode=&market=1&issuetype=1&industry_code=&Page=1&chklike=Y";
        result = requests.get(url,headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
        })
        df = pd.read_html(result.text)[0][:][1:]

        #整理資料
        mydata = []
        for index in range(len(df)):
            d = df.iloc[index]
            # 拉下來的資料是 0:頁面編號	1:國際證券編碼	2:有價證券代號	3:有價證券名稱	4:市場別	5:有價證券別	6:產業別	7:公開發行/上市(櫃)/發行日	8:CFICode	9:備註
            # 將資料整理成 Tuple (stockCode,stockName,market,issuetype,industry,offerTime,memo)
            data = (d[2],d[3],d[4],d[5],d[6],d[7],None)

            mydata.append(data)


        #寫入資料庫中
        StockModel().AddStock(mydata)