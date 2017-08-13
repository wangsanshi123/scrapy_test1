# -*- coding:utf-8 -*-
import re
import ssl
import urllib2

import lxml.html

url = 'http://money.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/{}.phtml?year={}&jidu={}'
stockid = '601006'
year = '2017'
jidu = '2'

user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = {'User-Agent': user_agent}
context = ssl._create_unverified_context()
response = None
try:
    request = urllib2.Request(url.format(stockid, year, jidu), headers=headers)
    response = urllib2.urlopen(request, context=context)
except urllib2.URLError, e:
    if hasattr(e, "code"):
        print e.code
    if hasattr(e, "reason"):
        print e.reason

target = response.read()

# print target

tree = lxml.html.fromstring(target)
td = tree.cssselect('tr td')
beginflag = False
target = year + "-"
list_temp = []
list_open = []
list_max = []
list_close = []
list_min = []
list_volume = []  # 交易量
list_amount = []  # 交易金额

if td:
    for item in td:
        if re.search(r'%s' % (target), item.text_content()):
            beginflag = True
        if beginflag:
            list_temp.append(item.text_content().strip())

i = 0
for item in list_temp:
    if i + 7 < len(list_temp) + 1:
        list_open.append(list_temp[i + 1])
        list_max.append(list_temp[i + 2])
        list_close.append(list_temp[i + 3])
        list_min.append(list_temp[i + 4])
        list_volume.append(list_temp[i + 5])
        list_amount.append(list_temp[i + 6])
        i = i + 7

for item in list_max:
    print item, "\n========="

print "最大值是：",max(list_max)
print "最小值是：",min(list_min)