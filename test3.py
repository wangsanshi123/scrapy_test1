# -*- coding:utf-8 -*-
import re
import urllib
import urllib2

page = 1
url = 'http://www.qiushibaike.com/hot/page/' + str(page)
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = {'User-Agent': user_agent}
try:
    request = urllib2.Request(url, headers=headers)
    response = urllib2.urlopen(request)
except urllib2.URLError, e:
    if hasattr(e, "code"):
        print e.code
    if hasattr(e, "reason"):
        print e.reason

target = response.read().decode("utf-8")
# print target
# 提取作者
# author = re.findall(r'<img.*?alt="(.*?)"', target, re.S)
# if author:
#     for item in author:
#         if item:
#             print item
#             print "========="
#         else:
#             print "kong "

# 提取内容
# content = re.findall(r'<div class="content">.*?<span>(.*?)</span>', target, re.S)

# if content:
#     for item in content:
#         if item:
#             print item
#             print '\n==================================='
#         else:
#             print "内容为空"

# 点赞数评论数



# class ="stats-vote" > < i class ="number" > 658 < / i > 好笑 < / span >


# print target
# vote = re.findall(r'<span class="stats-vote"><i class="number">(\d+)</i>', target, re.S)
# if vote:
#     for item in vote:
#         if item:
#             print item
#         else:
#             print "内容为空"
# else:
#     print 'vote为空'

# comment = re.findall(r'>\s+<i class="number">(\d+)</i> ', target)
# if comment:
#     for item in comment:
#         if item:
#             print item
#         else:
#             print "内容为空"
# else:
#     print 'comment为空'


# 神评论
# < div
#
#
# class ="main-text" >
#
#
# 旁边大姐的场子砸的快！狠！准！稳！[大笑]
# < div
#
#
# class ="likenum" >

# hot_comment = re.findall(r'<div class="main-text">(.*?)<div', target, re.S)
# if hot_comment:
#     for item in hot_comment:
#         if item:
#             print item
#         else:
#             print "内容为空"
# else:
#     print 'hot_comment为空'

all = re.findall(
    r'<img.*?alt="(.*?)".*?<div class="content">.*?'
    r'<span>(.*?)</span>.*?'
    r'<span class="stats-vote"><i class="number">(\d+)</i>.*?'
    r'>\s+<i class="number">(\d+)</i>.*?'
    r'<div class="main-text">(.*?)<div',
    target, re.S)
if all:
    for item in all:
        if item:
            print '作者：', item[0], '\n内容：', item[1].strip(), '\n点赞数: ', item[
                2], '\n评论数：', item[3], '\n神评：', item[
                4].strip(), '\n == == == == == == == == == == == == == == == == == == == = '
        else:
            print "内容为空"
else:
    print 'all为空'
