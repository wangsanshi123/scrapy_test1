# -*- coding:utf-8 -*-
import urllib
import urllib2
import re

import lxml.html
# 百度贴吧爬虫类
class BDTB:
    # 初始化，传入基地址，是否只看楼主的参数
    def __init__(self, baseUrl, seeLZ):
        self.baseURL = baseUrl
        self.seeLZ = '?see_lz=' + str(seeLZ)

    # 传入页码，获取该页帖子的代码
    def getPage(self, pageNum):
        try:
            url = self.baseURL + self.seeLZ + '&pn=' + str(pageNum)
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            # print response.read()
            return response
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print u"连接百度贴吧失败,错误原因", e.reason
                return None


baseURL = 'http://tieba.baidu.com/p/3138733512'
bdtb = BDTB(baseURL, 0)
target = bdtb.getPage(1).read().decode('utf-8')
print target
# 提取作者
tree = lxml.html.fromstring(target)
div = tree.cssselect('div.d_post_content j_d_post_content')
print len(div)
for item in div:
    print item.text_content(),'\n==================================='