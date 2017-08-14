#!/usr/bin/python
# -*- coding: utf-8 -*-
import warnings
import sqlite3
import pymysql

warnings.filterwarnings('ignore')
__author__ = 'yangsheng'

class DBUtil(object):
    def __init__(self, dbpath):
        self._dbpath = dbpath
        self._conn = sqlite3.connect(self._dbpath)

    def cursor_execute_one(self, sql):
        '''查询结果，逐行读取，yield模式'''
        cursor = self._conn.cursor()
        cursor.execute(sql)
        hasnext=True
        while hasnext:
            data = cursor.fetchone()
            if data:
                yield data
            else:
                hasnext=False

    def cursor_execute(self, sql):
        cursor = self._conn.cursor()
        cursor.execute(sql)
        datas = cursor.fetchall()
        cursor.close()
        return datas

    def cursor_execute_nosearch(self, sql, comm=False, datas=None):
        '''
        执行sql语句，非查询，没有返回
        :param sql:  sql语句
        :param comm:  是否commit
        :param datas
        :return:
        '''
        cursor = self._conn.cursor()
        if datas:
            cursor.execute(sql, datas)
        else:
            cursor.execute(sql)
        if comm:
            self._conn.commit()

    def commit(self):
        '''
        提交之前发生的更新操作
        :return:
        '''
        self._conn.commit()

class MysqlUtil(object):

    def __init__(self, dbhost, dbport, dbname, dbuser, dbpwd, charset='utf8'):
        self.dbhost = dbhost
        self.dbport = dbport
        self.dbname = dbname
        self.dbuser = dbuser
        self.dbpwd = dbpwd
        self.charset = charset
        self._conn = pymysql.connect(host=dbhost, port=dbport, db=dbname,
                                     user=dbuser, passwd=dbpwd, charset=charset)

    def cursor_execute_nosearch(self, sql, comm=False):
        '''
        执行sql语句，非查询，没有返回
        :param sql:  sql语句
        :param comm:  是否commit
        :return:
        '''
        cursor = self._conn.cursor()
        cursor.execute(sql)
        cursor.close()
        if comm:
            self._conn.commit()

    def cursor_execute(self, sql):
        cursor = self._conn.cursor()
        cursor.execute(sql)
        dataset = cursor.fetchall()
        cursor.close()
        return dataset

    def commit(self):
        self._conn.commit()

    def close(self):
        self._conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

