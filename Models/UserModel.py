#!/usr/bin/python
# -*- coding:utf-8 -*-

from Repository.SQLiteRepository import SQLiteRepository
from Models.dbModel import dbModel
import datetime

# 使用者模型
class UserModel(dbModel):
    "使用者模型"

    TABLENAME = 'users'

    def __init__(self):
        # 取得資料倉儲
        self.repo = SQLiteRepository()
        self.initTable()

    def getUser(self,userID):
        "取得使用者帳號"
        queryStr = f"select * from {self.TABLENAME} where id=?"
        dataArray = (userID,)
        return self.repo.query_one_sql(queryStr,dataArray)

    def getUserByTelegramID(self,telegramID):
        "取得使用者帳號"
        queryStr = f"select * from {self.TABLENAME} where telegramID=?"
        dataArray = (telegramID,)
        return self.repo.query_one_sql(queryStr,dataArray)

    def AddUser(self,dataDict):
        "建立使用者帳號"
        queryStr = f"Insert into {self.TABLENAME}(name,telegramID,createtime) Values(?,?,?);"
        dataArray = (dataDict['name'],dataDict['telegramID'],datetime.datetime.now())
        return self.repo.insert_sql(queryStr,dataArray)

    def UpdateUserName(self,dataDict):
        "更新使用者名稱"
        queryStr = f"Update {self.TABLENAME} set name=? where userID=?;"
        dataArray = (dataDict['name'],dataDict['id'])
        return self.repo.update_sql(queryStr,dataArray)  

    def initTable(self):
        "初始化資料表"
        conn = self.repo.getConn()
        c = conn.cursor()
        c.execute(f'CREATE TABLE IF NOT EXISTS {self.TABLENAME} (id INTEGER PRIMARY KEY AUTOINCREMENT \
                                                ,name text \
                                                ,telegramID text \
                                                ,createTime text)')
