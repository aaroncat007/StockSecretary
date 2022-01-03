#!/usr/bin/python
# -*- coding:utf-8 -*-

from Repository.SQLiteRepository import SQLiteRepository
from Models.dbModel import dbModel
import datetime

# 股票模型
class StockModel(dbModel):
    "股票模型"

    TABLENAME = 'stock'

    def __init__(self):
        # 取得資料倉儲
        self.repo = SQLiteRepository()
        self.initTable()

    def getStockByCode(self,stockCode):
        """
        查詢股票資料(透過股票代碼)
        stockCode : 股票代碼
        Returns: 
            Tuple 查詢的資料
        """
        queryStr = f"select * from {self.TABLENAME} where stockCode=?"
        data = (stockCode,)
        import pandas as pd
        import numpy as np
        allstock1 = pd.read_html('https://isin.twse.com.tw/isin/C_public.jsp?strMode=2',encoding='big5hkscs',header=0)
        allstock1 = allstock1[0]
        allstock1=allstock1[1:int(np.where(allstock1['有價證券代號及名稱'] == '上市認購(售)權證')[0])]
        allstock1=allstock1.drop(['國際證券辨識號碼(ISIN Code)','CFICode','備註'],axis = 1)
        allstock1['symbol']=allstock1['有價證券代號及名稱'].str.split('　').str.get(0)
        allstock1['Name']=allstock1['有價證券代號及名稱'].str.split('　').str.get(1)
        del allstock1['有價證券代號及名稱']
        allstock = pd.read_html('https://isin.twse.com.tw/isin/C_public.jsp?strMode=4',encoding='big5hkscs',header=0)
        allstock = allstock[0]
        allstock=allstock[int(np.where(allstock['有價證券代號及名稱'] == '股票')[0])+1:int(np.where(allstock['有價證券代號及名稱'] == '特別股')[0])]
        allstock=allstock.drop(['國際證券辨識號碼(ISIN Code)','CFICode','備註'],axis = 1)
        allstock['symbol']=allstock['有價證券代號及名稱'].str.split('　').str.get(0)
        allstock['Name']=allstock['有價證券代號及名稱'].str.split('　').str.get(1)
        del allstock['有價證券代號及名稱']
        allstock1=pd.concat((allstock1,allstock),axis=0)
        allstock1.reset_index(inplace=True, drop=False)
        data=allstock1[allstock1['symbol']==str(stockCode) ]

        return self.repo.query_one_sql(queryStr,data)

    def getStockByMarket(self,marketStr):
        """
        查詢股票資料(透過市場別)
        industryStr : 市場名稱
        Returns: 
            Array<Tuple> 查詢的資料集        
        """
        queryStr = f"select * from {self.TABLENAME} where marketStr=?"
        data = (marketStr,)
        import pandas as pd
        import numpy as np
        allstock1 = pd.read_html('https://isin.twse.com.tw/isin/C_public.jsp?strMode=2',encoding='big5hkscs',header=0)
        allstock1 = allstock1[0]
        allstock1=allstock1[1:int(np.where(allstock1['有價證券代號及名稱'] == '上市認購(售)權證')[0])]
        allstock1=allstock1.drop(['國際證券辨識號碼(ISIN Code)','CFICode','備註'],axis = 1)
        allstock1['symbol']=allstock1['有價證券代號及名稱'].str.split('　').str.get(0)
        allstock1['Name']=allstock1['有價證券代號及名稱'].str.split('　').str.get(1)
        del allstock1['有價證券代號及名稱']
        allstock = pd.read_html('https://isin.twse.com.tw/isin/C_public.jsp?strMode=4',encoding='big5hkscs',header=0)
        allstock = allstock[0]
        allstock=allstock[int(np.where(allstock['有價證券代號及名稱'] == '股票')[0])+1:int(np.where(allstock['有價證券代號及名稱'] == '特別股')[0])]
        allstock=allstock.drop(['國際證券辨識號碼(ISIN Code)','CFICode','備註'],axis = 1)
        allstock['symbol']=allstock['有價證券代號及名稱'].str.split('　').str.get(0)
        allstock['Name']=allstock['有價證券代號及名稱'].str.split('　').str.get(1)
        del allstock['有價證券代號及名稱']
        allstock1=pd.concat((allstock1,allstock),axis=0)
        allstock1.reset_index(inplace=True, drop=False)
        data=allstock1[allstock1['市場別']==str(marketStr) ]
        return self.repo.query_all_sql(queryStr,data)

    def getStockByIndustry(self,industryStr):
        """
        查詢股票資料(透過產業別)
        industryStr : 產業名稱
        Returns: 
            Array<Tuple> 查詢的資料集 
        """
        queryStr = f"select * from {self.TABLENAME} where industryStr=?"
        data = (industryStr,)
        import pandas as pd
        import numpy as np
        allstock1 = pd.read_html('https://isin.twse.com.tw/isin/C_public.jsp?strMode=2',encoding='big5hkscs',header=0)
        allstock1 = allstock1[0]
        allstock1=allstock1[1:int(np.where(allstock1['有價證券代號及名稱'] == '上市認購(售)權證')[0])]
        allstock1=allstock1.drop(['國際證券辨識號碼(ISIN Code)','CFICode','備註'],axis = 1)
        allstock1['symbol']=allstock1['有價證券代號及名稱'].str.split('　').str.get(0)
        allstock1['Name']=allstock1['有價證券代號及名稱'].str.split('　').str.get(1)
        del allstock1['有價證券代號及名稱']
        allstock = pd.read_html('https://isin.twse.com.tw/isin/C_public.jsp?strMode=4',encoding='big5hkscs',header=0)
        allstock = allstock[0]
        allstock=allstock[int(np.where(allstock['有價證券代號及名稱'] == '股票')[0])+1:int(np.where(allstock['有價證券代號及名稱'] == '特別股')[0])]
        allstock=allstock.drop(['國際證券辨識號碼(ISIN Code)','CFICode','備註'],axis = 1)
        allstock['symbol']=allstock['有價證券代號及名稱'].str.split('　').str.get(0)
        allstock['Name']=allstock['有價證券代號及名稱'].str.split('　').str.get(1)
        del allstock['有價證券代號及名稱']
        allstock1=pd.concat((allstock1,allstock),axis=0)
        allstock1.reset_index(inplace=True, drop=False)
        data=allstock1[allstock1['產業別']==str(industryStr) ]
        return self.repo.query_all_sql(queryStr,data)
        return self.repo.query_all_sql(queryStr,data)

    def AddStock(self,dataArray):
        """
        新增多筆股票
        dataArray <Class: Array<Tuple>>
        Array(stockCode,stockName,market,issuetype,industry,offerTime,memo)
        """
        queryStr = f"Insert into {self.TABLENAME} (stockCode,stockName,market,issuetype,industry,offerTime,memo) Values(?,?,?,?,?,?,?);"
        return self.repo.insert_many_sql(queryStr,dataArray)

    def initTable(self):
        """
        初始化資料表
        stockCode:股票代碼
        stockName:股票名稱
        market:市場別
        issuetype:證券別
        industry:產業別
        offerTime:公開發行日
        memo:備註
        """
        conn = self.repo.getConn()
        c = conn.cursor()
        c.execute(f'CREATE TABLE IF NOT EXISTS {self.TABLENAME} (id INTEGER PRIMARY KEY AUTOINCREMENT \
                                                ,stockCode text \
                                                ,stockName text \
                                                ,market text \
                                                ,issuetype text \
                                                ,industry text \
                                                ,offerTime text \
                                                ,memo text)')