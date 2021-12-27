#!/usr/bin/python
# -*- coding:utf-8 -*-

from Repository.SQLiteRepository import SQLiteRepository
from Models.dbModel import dbModel
import datetime

class FavouriteModel(dbModel):
    "使用者喜愛股票清單"

    TABLENAME = 'favourite'
    
    def __init__(self):
        self.repo = SQLiteRepository()
        self.initTable()

    def addUserStock(self,userID,stockCode):
        """
        新增使用者的喜愛股票
        UserID: 使用者代碼
        stockCode : 股票代碼
        Returns: 
            True or False
        """
        queryStr = f"INSERT INTO {self.TABLENAME} (userID,stockCode,createTime) VALUES(?,?,?);"
        data = (userID,stockCode,datetime.datetime.now())
        return self.repo.insert_sql(queryStr,data) > 0

    def removeUserStock(self,userID,stockCode):
        """
        移除使用者的喜愛股票
        UserID : 使用者代碼
        StockCode: 股票代碼
        Returns: 
            True or False
        """
        queryStr = f"DELETE from {self.TABLENAME} where userID=? AND stockCode=?"
        data = (userID,stockCode)
        return self.repo.delete_sql(queryStr,data) > 0

    def getUserStock(self,userID,stockCode):
        """
        查詢使用者的喜愛股票
        UserID : 使用者代碼
        StockCode: 股票代碼
        Returns: 
            Tuple 查詢的資料
        """
        queryStr = f"select * from {self.TABLENAME} where userID=? AND stockCode=?"
        data = (userID,stockCode)
        return self.repo.query_one_sql(queryStr,data)

    def listUserStock(self,userID):
        """
        列出使用者的喜愛股票
        UserID : 使用者代碼
        Returns: 
            Array<Tuple> 查詢的資料集
        """
        queryStr = f"select * from {self.TABLENAME} where userID=?"
        data = (userID,)
        return self.repo.query_all_sql(queryStr,data)

    def initTable(self):
        "初始化資料表"
        conn = self.repo.getConn()
        c = conn.cursor()
        c.execute(f'CREATE TABLE IF NOT EXISTS {self.TABLENAME} (id INTEGER PRIMARY KEY AUTOINCREMENT \
                                                ,userID int \
                                                ,stockCode text \
                                                ,createTime text)')