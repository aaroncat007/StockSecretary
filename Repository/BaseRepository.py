#!/usr/bin/python
# -*- coding:utf-8 -*-

from abc import ABCMeta, abstractmethod

# 基礎倉儲層
class BaseRepository(metaclass=ABCMeta):

    # 取得資料庫連線
    @abstractmethod
    def getConn(self):
        pass

    # 查詢單筆資料語法
    @abstractmethod
    def query_one_sql(self,queryStr,dataArray):
        pass

    # 查詢多筆資料語法
    @abstractmethod
    def query_all_sql(self,sqlstr):
        pass

    # 更新資料語法
    @abstractmethod
    def update_sql(self,updateStr,dataArray):
        pass

    # 新增資料語法
    @abstractmethod
    def insert_sql(self,InsertQueryStr,dataArray):
        pass

    # 刪除資料語法
    @abstractmethod
    def delete_sql(self,deleteQueryStr,dataArray):
        pass