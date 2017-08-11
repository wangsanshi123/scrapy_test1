# -*- coding:utf-8 -*-
import ssl
import urllib2

import lxml.html

page = 1
url = 'http://www.qiushibaike.com/hot/page/' + str(page)
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

target = response.read().decode("utf-8")
# print target

tree = lxml.html.fromstring(target)
div = tree.cssselect('div.content')
if div:
    for item in div:
        print item.text_content(),"\n============================"
