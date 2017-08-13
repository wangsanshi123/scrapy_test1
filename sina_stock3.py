# -*- coding:utf-8 -*-
import re
import ssl
import urllib2

import lxml.html


class GetStockCode:
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
            text = item.text_content().lstrip()
            result = re.search(r'\((.*?)\)', text)
            # result = re.search(r'(.*?)', text)
            if result:
                result_temp = result.group(0)
                list_stockcode = result_temp[1:len(result_temp)-1]
                list_stockcodes.append(list_stockcode)
        return list_stockcodes
        pass

    pass


# stockcodes = GetStockCode().getstockcode()
# for stockcode in stockcodes:
#
#     print stockcode