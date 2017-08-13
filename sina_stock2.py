# -*- coding:utf-8 -*-
import re
import ssl
import urllib2

import lxml.html
import time


class StockInfo:
    url = 'http://money.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/{}.phtml?year={}&jidu={}'

    year = '2017'
    jidu = '2'

    target = year + "-"

    # list_temp = []
    # list_open = []
    # list_max = []
    # list_close = []
    # list_min = []
    # list_volume = []  # 交易量
    # list_amount = []  # 交易金额

    def __init__(self):
        self.list_temp = []
        self.list_open = []
        self.list_max = []
        self.list_close = []
        self.list_min = []
        self.list_volume = []  # 交易量
        self.list_amount = []  # 交易金额

    def getData(self, stockcode, jidu):
        '''获取指定时间内的数据，如最近一个季度，最近四个季度，ps:只能已季度为单位'''
        self.stockcode = stockcode
        year = int(time.strftime('%Y-%m', time.localtime(time.time())).split('-')[0])
        jidu_current = int(time.strftime('%Y-%m', time.localtime(time.time())).split('-')[1]) / 3 + 1
        # jidu_temp = None
        # year_temp = None
        for i in range(jidu):
            if jidu_current - i > 0:
                jidu_temp = jidu_current - i
                year_temp = year
            else:
                jidu_temp = jidu_current + 1 - i
                year_temp = year - 1
                pass
            self.visiteSina(stockcode, year_temp, jidu_temp)

            pass
        # 将数据获得数据简单处理后存到内存中
        i = 0
        for item in self.list_temp:
            if i + 7 < len(self.list_temp) + 1:
                self.list_open.append(self.list_temp[i + 1])
                self.list_max.append(self.list_temp[i + 2])
                self.list_close.append(self.list_temp[i + 3])
                self.list_min.append(self.list_temp[i + 4])
                self.list_volume.append(self.list_temp[i + 5])
                self.list_amount.append(self.list_temp[i + 6])
                i += 7

    def price_info(self, day):
        '''行情,指定天数内的最大值，最小值相对于当今价格的涨跌比率'''
        # if len(self.list_max):
        if self.list_max:
            max_price = max(self.list_max[0:day])
            min_price = min(self.list_min[0:day])
            current_price = self.list_close[0]

            # print "%d天内的最大值是:" % (day), max_price
            # print "%d天内的最小值是：" % (day), min_price
            # print "当前值是：", current_price
            change_percent = (float(max_price) - float(current_price)) / float(max_price) * 100

            print "代码为%s当前值相对%d天内的最大值下跌了：" % (self.stockcode, day), str(change_percent), "%"
        else:
            print "无法获取代码为%s:" % (self.stockcode), "的股票信息"
        pass

    def visiteSina(self, stockcode, year, jidu):
        ''' 访问新浪，获得数据'''
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = {'User-Agent': user_agent}
        context = ssl._create_unverified_context()
        response = None
        try:
            request = urllib2.Request(self.url.format(stockcode, year, jidu), headers=headers)
            response = urllib2.urlopen(request, context=context)
        except urllib2.URLError, e:
            if hasattr(e, "code"):
                print e.code
            if hasattr(e, "reason"):
                print e.reason
        if response is None:
            print "无法抓取网页"

        else:
            target = response.read()
            tree = lxml.html.fromstring(target)
            td = tree.cssselect('tr td')
            beginflag = False
            split_target = str(year) + "-"
            if td:
                for item in td:
                    if re.search(r'%s' % (split_target), item.text_content()):
                        beginflag = True
                    if beginflag:
                        self.list_temp.append(item.text_content().strip())

        pass

    def getstockcode(self):
        list_stockcodes = []
        url = "http://quote.eastmoney.com/stocklist.html"
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = {'User-Agent': user_agent}
        context = ssl._create_unverified_context()
        response = None
        try:
            request = urllib2.Request(url, headers=headers)
            response = urllib2.urlopen(request, context=context)
        except urllib2.URLError, e:
            if hasattr(e, "code"):
                print e.code
            if hasattr(e, "reason"):
                print e.reason

        target = response.read()
        tree = lxml.html.fromstring(target)
        a = tree.cssselect('li a')
        for item in a:
            text = item.text_content().strip()
            result = re.search(r'\((.*?)\)', text)
            if result:
                list_stockcodes.append(result)
        return list_stockcodes
        pass

# StockInfo().getData('601006', 1)
# StockInfo().price_info(10)
#


# StockInfo.getData('601006', 1)
# StockInfo.price_info(10)


# stockinfo = StockInfo()
# stockinfo.getData('601006', 1)
# stockinfo.price_info(10)
