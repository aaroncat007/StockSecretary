#!/usr/bin/python
# -*- coding:utf-8 -*-

import sqlite3

from Repository.BaseRepository import BaseRepository

# SQLite 資料庫
class SQLiteRepository(BaseRepository):

    def __init__(self):
        super().__init__()
        # 初始化資料庫連線
        self.conn = sqlite3.connect('data.db')

    def getConn(self):
        "取得資料庫連線"
        myconn = self.conn
        return myconn

    def query_one_sql(self,queryStr,dataArray):
        """
        查詢單筆資料
        queryStr: 查詢資料的語法，資料欄位請用?代替以避免SQL injection
                  例如: SELECT * FROM Table WHERE A=?;
        dataArray: 資料欄位，依照?順序將資料放入其中 
                    例如: ('ABC')
        Returns: 
                  Object 查詢的資料 
        """
        # 拿到資料庫查詢指標
        conn = self.getConn()
        c = conn.cursor()

        # 執行查詢
        c.execute(queryStr,dataArray)
        queryResult = c.fetchone()
        return queryResult   

    def query_all_sql(self,queryStr,dataArray):
        """
        查詢多筆資料
        queryStr: 查詢資料的語法，資料欄位請用?代替以避免SQL injection
                  例如: SELECT * FROM Table WHERE A=?;
        dataArray: 資料欄位，依照?順序將資料放入其中 
                    例如: ('ABC')
        Returns: 
                  Array<Tuple> 查詢的資料集 
        """
        # 拿到資料庫查詢指標
        conn = self.getConn()
        c = conn.cursor()

        # 執行查詢
        c.execute(queryStr,dataArray)
        queryResult = c.fetchall()
        return queryResult

    def update_sql(self,updateStr,dataArray):
        """
        更新資料
        updateStr: 更新資料的語法，資料欄位請用?代替以避免SQL injection
                    例如: Update Table Set A=?,B=? WHERE C=?;
        dataArray: 資料欄位，依照?順序將資料放入其中 
                    例如: (A,B,C)
        Returns: 
                    rows Integer 成功的資料列數
        """
        # 拿到資料庫查詢指標
        conn = self.getConn()
        c = conn.cursor()

        # 執行寫入
        c.execute(updateStr,dataArray)
        conn.commit()

        # 查詢有多少ROW在上一次操作時受到影響
        rows = c.rowcount
        return rows

    def insert_sql(self,InsertQueryStr,data):
        """ 
        新增資料
        InsertQueryStr: 新增資料的語法，資料欄位請用?代替以避免SQL injection
                        例如: insert into user(username, password) values(?, ?);
        data: 資料欄位，依照?順序將資料放入其中 
                    例如: ('user','pwd')
        Returns: 
                    rows Integer 成功的資料列數 
        """
        # 拿到資料庫查詢指標
        conn = self.getConn()
        c = conn.cursor()

        # 執行寫入
        c.execute(InsertQueryStr,data)
        conn.commit()

        # 查詢有多少ROW在上一次操作時受到影響
        rows = c.rowcount
        return rows

    def insert_many_sql(self,InsertQueryStr,dataArray):
        """ 
        新增多筆資料
        InsertQueryStr: 新增資料的語法，資料欄位請用?代替以避免SQL injection
                        例如: insert into user(username, password) values(?, ?);
        dataArray: 資料欄位，依照?順序將資料放入其中 
                    例如: ('user','pwd')
        Returns: 
                    rows Integer 成功的資料列數 
        """
        # 拿到資料庫查詢指標
        conn = self.getConn()
        c = conn.cursor()

        # 執行寫入
        c.executemany(InsertQueryStr,dataArray)
        conn.commit()

        # 查詢有多少ROW在上一次操作時受到影響
        rows = c.rowcount
        return rows

    def delete_sql(self,deleteQueryStr,dataArray):
        """
        刪除資料
        updateStr: 更新資料的語法，資料欄位請用?代替以避免SQL injection
                    例如: DELETE FROM Table WHERE C=?;
        dataArray: 資料欄位，依照?順序將資料放入其中 
                    例如: ('1')
        Returns: 
                    rows Integer 成功的資料列數
        """
        # 拿到資料庫查詢指標
        conn = self.getConn()
        c = conn.cursor()

        # 執行寫入
        c.execute(deleteQueryStr,dataArray)
        conn.commit()

        # 查詢有多少ROW在上一次操作時受到影響
        rows = c.rowcount

        return rows