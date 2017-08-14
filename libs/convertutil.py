#!/usr/bin/python
# -*- coding: utf-8 -*-
import codecs
import sqlite3
import baseutil
import os
import time

class Excel2DB(object):
    '''
    将Excel数据转存入DB中
    '''
    def __init__(self, list_path, dest_db):
        self._title = None
        self._conn = None
        self._list_path = list_path
        self._dest_db = dest_db

    def convert(self):
        for excelpath in self._list_path:
            print('开始处理{0}'.format(excelpath))
            title, dataset = self.readall(excelpath)
            if not self._title:
                self._title=title
                self.initdb()
            self.insert(dataset)

    def readall(self, excelpath):
        if excelpath.endswith('.xls'):
            reader = baseutil.XlsReader(excelpath)
        elif excelpath.endswith('.xlsx'):
            reader = baseutil.XlsxReader(excelpath)
        sheetnames = reader.get_sheetnames()
        dataset_out = list()
        title = None
        for sheetname in sheetnames:
            dataset = reader.read_sheet(sheetname)
            dataset_out.extend(dataset[1:])
            title = dataset[0][:11]
        return title, dataset_out

    def initdb(self):
        exist = os.path.exists(self._dest_db)
        self._conn = sqlite3.connect(self._dest_db)
        if not exist:
            print('{0}不存在，初始化'.format(self._dest_db))
            # event_id	device_id	device_model	device_version	t_d	p_n	p_t	r_t	event_date	save_date	day
            sql_create = 'create table data ({0})'.format(', '.join(self._title))
            cursor = self._conn.cursor()
            cursor.execute(sql_create)
            self._conn.commit()
            cursor.close()

    def insert(self, dataset):
        cursor = self._conn.cursor()
        for data in dataset:
            sql = 'insert into data ({0}) values ({1})'.format(', '.join(self._title), (','.join(['?']*len(self._title))))
            cursor.execute(sql, data[:11])
        self._conn.commit()
        cursor.close()

    def close(self):
        if self._conn:
            self._conn.close()

class TxtSpliter(object):

    def __init__(self, src_txt_path, dest_txt_folder):
        self._src_txt_path = src_txt_path
        self._dest_txt_folder = dest_txt_folder
        if not self._dest_txt_folder.endswith('\\'):
            self._dest_txt_folder += '\\'
        if not os.path.exists(self._dest_txt_folder):
            os.makedirs(self._dest_txt_folder)

    def split(self, dataindex):
        txt_reader = baseutil.TxtReaderIter(self._src_txt_path)
        dict_file = dict()

        for data in txt_reader.readall():
            line = '\t'.join(data)
            if not data[dataindex] in dict_file:
                dict_file[data[dataindex]] = baseutil.TxtWriter(self.__gen_filepath(data[dataindex]))
            dict_file[data[dataindex]].writeline(line)

        for item in dict_file.items():
            item[1].close()

    def __gen_filepath(self, model):
        return '%s%s.txt'%(self._dest_txt_folder, model)

class Txt2ExcelSimple(object):

    ROWNUM_EACHSHEET = 65000

    def __init__(self, src_txt_path, dest_xlsx_path):
        self._src_txt_path = src_txt_path
        self._dest_xlsx_path = dest_xlsx_path

    def convert(self, rownum_eachsheet=ROWNUM_EACHSHEET, title=None):
        txt_reader = baseutil.TxtReaderIter(self._src_txt_path)
        wb = baseutil.WorkBook(self._dest_xlsx_path)
        row = 0
        index = 0
        dataset_temp = list()
        for data in txt_reader.readall():
            row += 1
            dataset_temp.append(data)
            if row >= rownum_eachsheet:
                if title:
                    dataset_temp.insert(0, title)
                print('写入sheet %s，数据量%s'%(index, len(dataset_temp)))
                wb.add_sheet('%s'%index, dataset_temp)
                row = 0
                dataset_temp = list()
                index += 1
        if dataset_temp:
            if title:
                dataset_temp.insert(0, title)
            print('写入sheet %s，数据量%s'%(index, len(dataset_temp)))
            wb.add_sheet('%s' % index, dataset_temp)
        wb.close()

class Txt2Excel(object):

    ROWNUM_EACHXLSX = 65000

    def __init__(self, src_txt_path, dest_xlsx_folder):
        self._src_txt_path = src_txt_path
        self._dest_xlsx_folder = dest_xlsx_folder
        if not self._dest_xlsx_folder.endswith('\\'):
            self._dest_xlsx_folder += '\\'
        if not os.path.exists(self._dest_xlsx_folder):
            os.makedirs(self._dest_xlsx_folder)

    def convert(self, rownum_eachxlsx=ROWNUM_EACHXLSX, title=None):
        txt_reader = baseutil.TxtReaderIter(self._src_txt_path)
        row = 0
        index = 0
        dataset_temp = list()
        for data in txt_reader.readall():
            row += 1
            dataset_temp.append(data)
            if row >= rownum_eachxlsx:
                if title:
                    dataset_temp.insert(0, title)
                self.__write_excel(dataset_temp, self.__gen_xlsxpath(index))
                row = 0
                dataset_temp = list()
                index += 1
        if dataset_temp:
            if title:
                dataset_temp.insert(0, title)
            self.__write_excel(dataset_temp, self.__gen_xlsxpath(index))

    def __gen_xlsxpath(self, index):
        return '%s%s.xlsx'%(self._dest_xlsx_folder, index)

    def __write_excel(self, dataset, xlsx_path):
        print('写入%s, %s条数据'%(xlsx_path, len(dataset)-1))
        wb = baseutil.WorkBook(xlsx_path)
        wb.add_sheet('sheet', dataset)
        wb.close()


def convert_chenguanghui():
    models = ['X6A', 'X6D', 'X6PlusA', 'X6SA', 'X6SPlusA', 'Y51']
    models = ['Xplay5A']
    folder_root = r'F:\工作\用户标签\用户行为数据_20160629\结果数据'
    for model in models:
        print('开始处理%s'%model)
        folder = '%s\\%s'%(folder_root, model)
        list_path = baseutil.get_filelist(folder, 'xls') + baseutil.get_filelist(folder, 'xlsx')
        db_path = '%s\\%s\\%s_behavior.db'%(folder_root, model, model)
        converter = Excel2DB(list_path, db_path)
        converter.convert()
        converter.close()


def findimei():
    patha = r'F:\工作\用户标签\用户模型_20160601\xplay5a源数据\一线城市\Xplay5A\behavior.db'
    conn = sqlite3.connect(patha)
    cur = conn.cursor()
    cur.execute('select distinct device_id from data limit 2500')
    dataset = cur.fetchall()
    imeis = [x[0] for x in dataset]
    print('\n'.join(imeis))

def get_xplay5a_0613_0615():
    patha = r'F:\工作\用户标签\用户模型_20160601\xplay5a源数据\一线城市\Xplay5A\behavior.db'
    imei_path = r'F:\工作\用户标签\用户行为数据_20160629\Xplay5A_imei_2500.txt'
    imeilist = baseutil.TxtReader(imei_path).readall(baseutil.TxtReader.SRC_TYPE_NORMAL).split()
    print('共有IMEI %s'%len(imeilist))
    conn = sqlite3.connect(patha)
    cur = conn.cursor()
    sql = "select * from data where device_id in (%s)"%(','.join(["'%s'"%x for x in imeilist]))
    print(sql)
    cur.execute(sql)
    # dataset = cur.fetchall()
    # print('共查询到数据%s'%len(dataset))
    count = 0
    dataset_temp = list()
    titles = ['event_id','device_id','device_model','device_version','t_d','p_n','p_t','r_t','event_date','save_date','day']

    def write_xlsx(ds):
        folder_root = r'F:\工作\用户标签\用户行为数据_20160629\结果数据\Xplay5A'
        timestr = '%s'%int(time.time() * 1000)
        path_out = '%s\\%s.xlsx'%(folder_root, timestr)
        ds_out = [titles] + ds
        wb = baseutil.WorkBook(path_out)
        wb.add_sheet('sheet', ds_out)
        wb.close()
        print('写入完毕%s'%path_out)

    while True:
        data = cur.fetchone()
        if not data:
            break
        count += 1
        dataset_temp.append(data)
        if count > 65300:
            write_xlsx(dataset_temp)
            dataset_temp = list()
            count = 0
    write_xlsx(dataset_temp)


def convert_beiguang():
    txt_folder = r'F:\工作\用户行为数据_SQL\gallery_0623-0725'
    model_txts = baseutil.get_filelist(txt_folder, 'txt')
    for model_txt in model_txts:
        print('开始处理%s'%model_txt)
        model = os.path.basename(model_txt)[:-4]
        dest_folder = r'%s\%s'%(txt_folder, model)
        Txt2Excel(model_txt, dest_folder).convert(
            title=['device_id', 'device_model', 'device_version', 'event_id', 'event_label', 'event_time', 'event_date',
                   'start_time', 'start_date', 'end_time', 'end_date', 'use_number', 'duration', 'save_date', 'params',
                   'day'])

def convert_split_model():
    '''
    将一个 txt 文件中的数据 按照机型划分为 分机型的 txt文件
    :return:
    '''
    # txt_folder = r'F:\工作\用户行为数据_SQL\public_view_0623_0722_v3_v3maxa_xplay5a'
    # txt_dest_folder = r'F:\工作\用户行为数据_SQL\public_view_0623_0722'
    # for txt_path in baseutil.get_filelist(txt_folder, 'txt'):
    #     print('开始处理%s'%txt_path)
    #     TxtSpliter(txt_path, txt_dest_folder).split(1)

    txt_path = r'F:\工作\用户行为数据_SQL\超级截屏\screenshot_x5max+_y51_0905_0918_new.txt'
    txt_dest_folder = r'F:\工作\用户行为数据_SQL\超级截屏\screenshot_x5max+_y51_0905_0918_new_models'
    TxtSpliter(txt_path, txt_dest_folder).split(1)

def convert_split(same_xlsx=True):
    '''
    将 txt 文件分拆为 xlsx 列表
    :return:
    '''
    txt_path = r'F:\工作\用户行为数据_SQL\fingerprint_x7\fingerprint_x7_x7plus_0829_0904\vivo X7.txt'
    dest_folder = r'F:\工作\用户行为数据_SQL\fingerprint_x7\fingerprint_x7_x7plus_0829_0904\vivo X7'
    if same_xlsx:
        Txt2ExcelSimple(txt_path, dest_folder).convert(title=['device_id','device_model','device_version','event_id','event_label','event_time','event_date','start_time','start_date','end_time','end_date','use_number','duration','save_date','params','day'])
    else:
        Txt2Excel(txt_path, dest_folder).convert(title=['device_id','device_model','device_version','event_id','event_label','event_time','event_date','start_time','start_date','end_time','end_date','use_number','duration','save_date','params','day'])

def convert_split_new():
    txt_path_1 = r'F:\工作\用户行为数据_SQL\userbehave_xplay5a_imei.txt'
    txt_path_2 = r'F:\工作\用户行为数据_SQL\userbehave_xplay5a_imei_506.txt'
    dest_folder_1 = r'F:\工作\用户行为数据_SQL\userbehave_xplay5a_imei'
    dest_folder_2 = r'F:\工作\用户行为数据_SQL\userbehave_xplay5a_imei_506'

    Txt2Excel(txt_path_1, dest_folder_1).convert(title=['device_id','device_model','device_version','event_id','event_label','event_time','event_date','start_time','start_date','end_time','end_date','use_number','duration','save_date','params','day'])
    Txt2Excel(txt_path_2, dest_folder_2).convert(title=['event_id','device_id','device_model','device_version','t_d','p_n','p_t','r_t','event_date','save_date','day'])

def main():
    # folder = r'F:\工作\用户标签\用户模型_20160601\xplay5a源数据\一线城市\Xplay5A\xls源'
    folder = r'F:\工作\用户标签\用户模型_20160601\xplay5a源数据\一线城市\Xplay5A\xls源_0615\1467337589442'
    list_path = baseutil.get_filelist(folder, 'xls') + baseutil.get_filelist(folder, 'xlsx')
    db_path = r'F:\工作\用户标签\用户模型_20160601\xplay5a源数据\一线城市\Xplay5A\behavior.db'
    converter = Excel2DB(list_path, db_path)
    converter.convert()
    converter.close()

if __name__ == '__main__':
    # convert_chenguanghui()
    # findimei()
    # get_xplay5a_0613_0615()
    # convert_beiguang()
    # convert_split(False)
    convert_split_model()
    # convert_split_new()