# -*- coding:utf-8 -*-
import csv
import re

import time

from link_crawler import Throttle
from sina_stock3 import GetStockCode
from sina_stock5_csv import StockInfo


class Sina_stock:
    def getlastUpdateInfo(self):
        '''读取stockdata.csv文件，读取最近时间，然后和当前时间比较，判断应该读取的的开始时间(应该读取的季度数),返回值为应该读取的季度数和上次爬取的时间'''
        # 确定上次爬取的时间
        last_year = None
        last_month = None
        jidu = None  # 应该爬取的季度
        with open('stockdata_1.csv', 'U') as f:
            f_csv = csv.reader(f)
            for row in f_csv:
                date = row[1]
                if re.match(r'201.*?', date):
                    last_year = int(date[0:4])
                    last_month = int(date[5:7])
                    break
        # 比交当前时间和最后爬取的时间

        year = int(time.strftime('%Y-%m', time.localtime(time.time())).split('-')[0])
        month = int(time.strftime('%Y-%m', time.localtime(time.time())).split('-')[1])
        jidu_current = int(time.strftime('%Y-%m', time.localtime(time.time())).split('-')[1]) / 3 + 1
        # print year, month, jidu_current,'\n'
        # print last_year,last_month
        if month >= last_month:
            jidu = (month - last_month) / 3 + 2 + (year - last_year) * 4
        else:
            jidu = (month + 12 - last_month) / 3 + (year - 1 - last_year) * 4
        return jidu, date

    def getDataAndSave_first(self, stockcodes):
        ''' 读取所有股票的数据，并存入csv文件中,第一次时调用（获取原始数据）  '''
        i = 0
        for stockcode in stockcodes:
            i += 1
            if i < 500:
                data = StockInfo().getData(stockcode, 12, 4)
                with open('stockdata_1.csv', 'a') as f:
                    f_csv = csv.writer(f)
                    f_csv.writerows(data)
                pass

        pass

    def getstockcodesFromInternet(self):
        '''从网络上获取股票代码并存入本地文件中'''
        stockcodes = GetStockCode().getstockcode()
        for item in stockcodes:
            print item
        with open('stockcodes.csv', 'w') as f:
            f_csv = csv.writer(f)
            f_csv.writerows(stockcodes)

    def getstockcodesFromDisk(self):
        '''从本地磁盘获取股票代码'''
        codes_list = []
        with open('stockcodes.csv', 'U') as f:
            f_csv = csv.reader(f)
            for row in f_csv:
                if re.search(r'\d', ''.join(row)):
                    codes_list.append(''.join(row))

        return codes_list

    def updateData(self):  # 关键方法
        '''更新数据:'''
        jidu = self.getlastUpdateInfo()[0]
        date = self.getlastUpdateInfo()[1]
        list_all_new = []
        with open('stockdata_1.csv', 'U') as f:
            # 获取股票代码
            f_csv = csv.reader(f)
            position = 0  # 插入更新信息的位置
            for row in f_csv:
                if re.match(r'\d', ''.join(row)):
                    stockcode = row[0]
                    # 将从disk里面读取的数据临时存到内存中
                    list_all_new.append(row)
                    if stockcode is not None and stockcode is  row[0]:
                        # 获取当前股票最新数据并存入csv文档中
                        datas = StockInfo().getData(stockcode, jidu, 4)
                        # 分析数据，根据日期去掉重复部分，然后存入csv文档中
                        i = 0

                        list_single_new = []  # 单只股票更新的信息
                        for item in datas:
                            # 将从网络上的得到的数据存到内存中
                            list_single_new.append(item)
                            if i % 7 == 0:
                                list_co = datas[i:i + 7]
                                list_single_new.append(list_co)

                            if item[0] == date:
                                break
                            i += 1
                        pass
                        list_all_new.insert(position, list_single_new)
                    position += 1
        print len(list_all_new)
        print list_all_new[0]

        pass


if __name__ == '__main__':
    stock = Sina_stock()

    # Sina_stock().fun1('601006')
    # print Sina_stock().fun2()[0]
    # print Sina_stock().fun2()[1]
    # Sina_stock().getstockcodesFromInternet()

    # codes = stock.getstockcodesFromDisk()
    # stock.getDataAndSave(codes)

    stock.updateData()
