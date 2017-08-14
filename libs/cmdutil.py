#!/usr/bin/python
# -*- coding: utf-8 -*-
import warnings

import baseutil

warnings.filterwarnings('ignore')
__author__ = 'yangsheng'


class Hive(object):
    '''
    Hive命令操作工具
    '''
    @staticmethod
    def runsql(sql, file=None):
        '''
        Hive中运行sql
        :param sql: sql语句
        :param file: 把结果写入文件的路径
        :return:
        '''
        if file:
            cmd = 'hive -e "{0}" > {1}'.format(sql, file)
        else:
            cmd = 'hive -e "{0}"'.format(sql)
        result = baseutil.runshell(cmd)
        return [x.strip() for x in result]

    @staticmethod
    def runfile(sql_path, file=None):
        '''
        Hive中运行sql文件
        :param sql_path: sql文件路径
        :param file: 把结果写入文件的路径
        :return:
        '''
        if file:
            cmd = 'hive -f "{0}" > {1}'.format(sql_path, file)
        else:
            cmd = 'hive -f "{0}"'.format(sql_path)
        result = baseutil.runshell(cmd)
        return [x.strip() for x in result]

    @staticmethod
    def get_firstparts(tablename):
        '''
        获取Hive表的分区列表，若有多个分区字段，则只获取第一个分区字段列表，不去重
        :param tablename: Hive表，需包含库名
        :return:
        '''
        sql = '''show partitions {0}'''.format(tablename)
        result = Hive.runsql(sql)
        return [x.split('/')[0].split('=')[1].strip() for x in result]


class Hive2Mysql(object):
    '''
    伪sqoop，把Hive中的数据查询之后插入到mysql中
    '''
    def __init__(self, dbcon):
        self.dbcon = dbcon

    def transfer(self, sql_hive, tmpfile, tablename, columns):
        '''
        开始传输
        :param sql_hive: 导出Hive的sql
        :param tmpfile: 临时中转文件路径
        :param tablename: mysql目的表
        :param columns: mysql字段列表
        :return:
        '''
        Hive.runsql(sql_hive, tmpfile)

        for data in baseutil.TxtReader(tmpfile).readall():
            if not data:
                continue
            if not len(data) == columns:
                raise Exception('hive查询结果的列数必须与columns数相同')
            sql_insert = '''
            insert into {0} ({1})
            values ('{2}')
            '''.format(tablename, ','.join(columns), "','".join(data))
            self.dbcon.cursor_execute(sql_insert)
        self.dbcon.commit()


class Mysql2Hive(object):
    '''
    伪sqoop，把mysql中的数据查询之后导入到Hive中
    '''
    def __init__(self, dbcon):
        self.dbcon = dbcon

    def transfer(self, hivetable, partition, tmpfile, sql_export):
        '''
        开始传输
        :param hivetable: 导入到hive中
        :param partition: hive分区，格式：{'day':'2017-06-01'}
        :param tmpfile: 临时中转文件路径
        :param sql_export: 导出mysql数据的sql
        :return:
        '''
        cmd_export = '''mysql -u{0} -p{1} {2} -h{3} -N -e "{4}" > {5}'''\
            .format(self.dbcon.dbuser, self.dbcon.dbpwd, self.dbcon.dbname, self.dbcon.dbhost,
                    sql_export, tmpfile)
        baseutil.runshell(cmd_export)
        if partition:
            prt_items = partition.items()
            prtlst = ["{0}='{1}'".format(prt[0], prt[1]) for prt in prt_items]
            prt_str = ', '.join(prtlst)
            hive_import = '''load data local inpath '{0}' overwrite into table {1} partition ({2})'''.format(tmpfile, hivetable, prt_str)
        else:
            hive_import = '''load data local inpath '{0}' overwrite into table {1}'''.format(tmpfile, hivetable)
        Hive.runsql(hive_import)




class Python(object):

    def __init__(self, pypath):
        self.pypath = pypath

    def runscript(self, scriptpath, logpath=None):
        if logpath:
            cmd = '{0} {1}'.format(self.pypath, scriptpath, logpath)
        else:
            cmd = '{0} {1}'.format(self.pypath, scriptpath)
        result = baseutil.runshell(cmd)
        return [x.strip() for x in result]






