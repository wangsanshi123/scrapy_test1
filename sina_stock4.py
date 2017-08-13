# -*- coding:utf-8 -*-

from link_crawler import Throttle
from sina_stock2 import StockInfo
from sina_stock3 import GetStockCode

stockcodes = GetStockCode().getstockcode()

i =0
delay =4
throttle = Throttle(delay)
for stockcode in stockcodes:
    i+=1
    if i<500:
        throttle.wait('http://money.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/')
        stockinfo = StockInfo()
        stockinfo.getData(str(stockcode), 1)
        stockinfo.price_info(10)

# stockinfo = StockInfo()
# stockinfo.getData('201000', 1)
# # stockinfo.getData('601006', 1)
# stockinfo.price_info(10)
