#!/usr/bin/python
# -*- coding:utf-8 -*-

from Repository.SQLiteRepository import SQLiteRepository
from Models.dbModel import dbModel
import datetime

# 股票模型
class StockMonitorModel(dbModel):
    "股票監測模型"

    TABLENAME = 'stockMonitor'

    def __init__(self):
        self.repo = SQLiteRepository()
        self.initTable()

    def addUserStockMonitor(self,userID,stockCode,StockMonitorKind,StockMonitorCompare,triggerValue):
        """
        新增使用者的監測股票
        :param UserID: 使用者代碼
        :param stockCode: 股票代碼
        :param triggerKind: 監測類型
        :param triggerCompare: 監測比較方式
        :param triggerValue: 監測值
        :returns: 
            True or False
        """
        queryStr = f"INSERT INTO {self.TABLENAME} (userID,stockCode,triggerKind,triggerCompare,triggerValue,isEnable,createTime) VALUES(?,?,?,?,?,?,?);"
        data = (userID,stockCode,StockMonitorKind,StockMonitorCompare,triggerValue,1,datetime.datetime.now())
        return self.repo.insert_sql(queryStr,data) > 0

    def removeUserStockMonitorByID(self,stockMonitorID):
        """
        移除使用者的監測股票
        :param stockMonitorID: 股票監測代碼
        Returns: 
            True or False
        """
        queryStr = f"DELETE from {self.TABLENAME} where id=?"
        data = (stockMonitorID,)
        return self.repo.delete_sql(queryStr,data) > 0

    def removeUserStockMonitorByStock(self,userID,stockCode):
        """
        移除使用者的監測股票
        :param UserID: 使用者代碼
        :param StockCode: 股票代碼
        :returns: 
            True or False
        """
        queryStr = f"DELETE from {self.TABLENAME} where userID=? AND stockCode=?"
        data = (userID,stockCode)
        return self.repo.delete_sql(queryStr,data) > 0


    def getUserStockMonitorByID(self,stockMonitorID):
        """
        取得監測股票
        UserID : 使用者代碼
        Returns: 
            Tuple 查詢的資料
        """
        queryStr = f"select * from {self.TABLENAME} where id=?"
        data = (stockMonitorID,)
        return self.repo.query_one_sql(queryStr,data)

    def getUserStockByStock(self,userID,stockCode):
        """
        查詢使用者的監測股票(透過使用者與股票)
        UserID : 使用者代碼
        StockCode: 股票代碼
        Returns: 
            Array<Tuple> 查詢的資料
        """
        queryStr = f"select * from {self.TABLENAME} where userID=? AND stockCode=?"
        data = (userID,stockCode)
        return self.repo.query_all_sql(queryStr,data)

    def listUserStockMonitor(self,userID):
        """
        列出使用者的全部監測股票
        UserID : 使用者代碼
        Returns: 
            Array<Tuple> 查詢的資料集
        """
        queryStr = f"select * from {self.TABLENAME} where userID=?"
        data = (userID,)
        return self.repo.query_all_sql(queryStr,data)

    def getUserStockMonitorAvailable(self,userID):
        """
        列出使用者已啟用的股票監測
        :param userID: 使用者代碼
        """
        queryStr = f"select * from {self.TABLENAME} where userID=? AND isEnable=1;"
        data = (userID,)
        return self.repo.query_all_sql(queryStr,data)

    def enableStockMonitor(self,stockMonitorID):
        """
        啟用股票監測
        :param stockMonitorID: 股票監測代碼
        :returns:
            True or False
        """
        queryStr = f"UPDATE {self.TABLENAME} SET isEnable=1 where id=?"
        data = (stockMonitorID,)
        return self.repo.update_sql(queryStr,data)      

    def disableStockMonitor(self,stockMonitorID):
        """
        停用股票監測
        :param stockMonitorID: 股票監測代碼
        :returns:
            True or False
        """
        queryStr = f"UPDATE {self.TABLENAME} SET isEnable=0 where id=?"
        data = (stockMonitorID,)
        return self.repo.update_sql(queryStr,data) 

    def getAllEnStockMonitor(self):
        """
        取得所有已啟用的股票監測
        :returns:
            Array<Tuple>
        """
        queryStr = f"SELECT * FROM {self.TABLENAME} Where isEnable=?"
        data = (1,)
        return self.repo.query_all_sql(queryStr,data)        

    def initTable(self):
        """
        初始化資料表
        id: primary key
        userID: 使用者ID
        stockCode: 股票代碼
        triggerKind: 觸發類型
        triggerCompare: 觸發方式
        triggerValue: 觸發值
        isEnable: 是否啟用
        createTime: 建立時間
        """
        conn = self.repo.getConn()
        c = conn.cursor()
        c.execute(f'CREATE TABLE IF NOT EXISTS {self.TABLENAME} (id INTEGER PRIMARY KEY AUTOINCREMENT \
                                                ,userID int \
                                                ,stockCode text \
                                                ,triggerKind text \
                                                ,triggerCompare text \
                                                ,triggerValue text \
                                                ,isEnable INTEGER \
                                                ,createTime text)')

class StockMonitorKind:
    "監測類型"

    closing_price = "成交價"

    rise_fall_price = "漲跌價"

    rise_fall_rate = "漲跌幅度"

    trading_volume = "成交量"

    single_volume = "單量"

class StockMonitorCompare:
    "監測比較方式"

    greater_than = "gt"
    "大於"

    less_than = "lt"
    "小於"