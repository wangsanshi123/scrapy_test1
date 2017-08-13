# -*- coding:utf-8 -*-
import urllib
import urllib2
import re


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

# 提取作者
# author = re.findall(r'<img.*?username="(.*?)".*?class', target, re.S)
# if author:
#     for item in author:
#         print item
# else:
#     print 'author为空'



# 提取内容

# <div id="post_content_53018899389" class="d_post_content j_d_post_content ">
#                                                 第一次2L<img pic_type="1"
#                                                           src="https://tb2.bdstatic.com/tb/editor/images/face/i_f25.png?t=20140602"
#                                                           class="BDE_Smiley" height="29" width="29"></div>
#                                             <br></cc>

# content = re.findall(r'class="d_post_content j_d_post_content ">[.*?<img.*?>|\s+](.*?)[<img|</div>]', target, re.S)
content = re.findall(r'class="d_post_content j_d_post_content "(.*?)/div>', target, re.S)
# content = re.findall(r'class="d_post_content j_d_post_content ">.*?>?(.*?)+<?.*?</div>', target, re.S)

if content:

    for item in content:
        patch = re.findall(r'.*?>(.*?)<', item, re.S)

        print ''.join(patch).strip(), "\n+++++++++++++++++"
        pass

else:
    print 'content为空'
