# -*- coding:utf-8 -*-
import re
import ssl
import urllib2

import lxml.html
import time

from link_crawler import Throttle


class StockInfo:
    url = 'http://money.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/{}.phtml?year={}&jidu={}'

    year = '2017'
    jidu = '2'

    target = year + "-"

    def getData(self, stockcode, jidu, delay=5):
        '''获取指定时间内的数据，如最近一个季度，最近四个季度，ps:只能已季度为单位'''
        list_result = []
        list_temp = []
        year = int(time.strftime('%Y-%m', time.localtime(time.time())).split('-')[0])
        jidu_current = int(time.strftime('%Y-%m', time.localtime(time.time())).split('-')[1]) / 3 + 1
        # jidu_temp = None
        # year_temp = None
        throttle = Throttle(delay)
        for i in range(jidu):
            if jidu_current - i > 0:
                jidu_temp = jidu_current - i
                year_temp = year
            else:
                jidu_temp = jidu_current + 1 - i
                year_temp = year - 1
                pass

            list_temp.extend(self.visiteSina(stockcode, year_temp, jidu_temp, throttle))

            pass
        # 将数据获得数据简单处理后存到内存中
        list_temp2 = [stockcode]
        for i in range(len(list_temp)):
            if i % 7 == 0:
                list_co = list_temp2 + list_temp[i:i + 7]
                list_result.append(list_co)
        return list_result

    def visiteSina(self, stockcode, year, jidu, throttle):
        ''' 访问新浪，获得数据'''
        list_temp = []
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = {'User-Agent': user_agent}
        context = ssl._create_unverified_context()
        response = None

        throttle.wait(self.url.format(stockcode, year, jidu))
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
                        list_temp.append(item.text_content().strip())
        print '正在爬取数据：', stockcode, '年：', year, "度：", jidu
        return list_temp
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
