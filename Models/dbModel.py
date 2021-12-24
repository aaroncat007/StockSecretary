#!/usr/bin/python
# -*- coding:utf-8 -*-

from abc import ABCMeta, abstractmethod

class dbModel(metaclass=ABCMeta):

    # 初始化資料表
    @abstractmethod
    def initTable(self):
        pass