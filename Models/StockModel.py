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