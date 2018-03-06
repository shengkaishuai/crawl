# coding=utf-8
import scrapy
import pymongo
from doubanspider.items import DoubanspiderItem
from bs4 import BeautifulSoup
from scrapy.selector import Selector
import time
max_page = 5


# 思路：先得到每本书的短评的url，再进入每本书的短评界面，爬取每页的评论，爬5页
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


class MyDoubanSpider(scrapy.Spider):
    name = 'comments'

    def start_requests(self):

        all_books = [1770782,1084336,1008145,25862578,1082154,3259440,1046265,3211779,2567698,1017143,1007305,1016300,1040771,20427187,6082808,5275059,1461903,1200840,1141406,1041007,10554308,3066477,1068920,4238362,5363767,4242172,1083428,1090043,1026425,2256039,1873231,1071241,3995526,1400705,1039487,1041482,1023045,1059406,2209098,1022060,3879301,4886245,1529893,1009257,1057244,1858513,1066462,4913064,1082334,25747921,2062200,3646172,1255625,4074636,1049219,1432596,2250587,1045818,1029791,1049189,1361264,1948901,10594787,1013129,2022979,26340138,3426869,1059419,1050339,1085860,1007914,1019568,1089243,1003000,1401425,1119522,1002299,1775691,3813669,3369793,2143732,1064275,2340100,1082387,3608208,1040211,3191328,1465324,1786670,2256438,1080370,1024217,1255624,1453210,1013380,1082518,3394338,1065970,3598313,1827374,2159042,4714734,6388661,1029159,3369600,1949338,1030052,2154960,5317075,10763902,3014576,1054685,1085799,1794620,1205370,1016003,1221515,1060068,1024197,1829226,2053249,26382433,4117922,2243213,5916880,1056733,1039752,1013502,1014278,1856285,4011670,1882933,1046209,1449351,3616310,1596305,1291760,1227838,4009552,1917972,1044547,3674537,1358873,2052448,1029111,2331434,1963684,1020459,2081876,1962929,25985021,3006581,1346815,1008988,2056749,1016523,3344676,3071717,6710437,1812439,26278687,1058234,1703544,4124727,1012611,2057285,2253642,4238754,2035179,1469051,1212893,1086249,1006881,1034108,1009160,5414391,2339950,4113090,1926700,1204889,1088065,25984204,1963310,26356948,1082406,3009821,1043815,2298149,1051193,1043008,1013208,4010969,1080309,1018153,1027191,25924253,4038164,3017857,4166819,4874131,1474773,4231381,4207781,5327697,1205054,3266344,2139305,1292416,2070844,1767945,4908885,24934182,6798611,1863930,1082349,2567919,1007334,1059336,1063190,1431836]
        # all_books = [10519369]
        page = 1
        for bookid in all_books:
            # url = 'https://book.douban.com/subject/{}/reviews'.format(bookid)

            url = 'https://book.douban.com/subject/{}/comments/hot?p={}'.format(bookid, page)  # 实现翻页
            yield scrapy.Request(url=url, headers={'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.5; rv:10.0.1) Gecko/20100101 Firefox/10.0.1 SeaMonkey/2.7.1'}, meta={'book_id': bookid,'page':1})

    def parse(self, response):
        selector = Selector(response)
        comments = selector.xpath('//*[@id="comments"]/ul/li')   # 这里提取出来的是个列表
        bookid = response.meta['book_id']
        # print comments
        for comment in comments:
            print comment
            item = DoubanspiderItem()
            item['bookid'] = 'https://book.douban.com/subject/' + str(bookid)
            print item['bookid']
            try:
                item['comment'] = comment.xpath('div[2]/p/text()').extract()[0].encode('utf-8')  # /text()可以只把文本出来
                print item['comment']
            except:
                item['comment'] = "没有评论信息"
                print "没有评论信息"
            yield item
            time.sleep(0.05)
        if response.meta['page'] < max_page:
            page = response.meta['page'] + 1
            url = 'https://book.douban.com/subject/{}/comments/hot?p={}'.format(bookid, page)
            print 'page:', page
            yield scrapy.Request(url=url, headers={'user-agent': 'Mozilla/5.0'}, meta={'book_id': bookid, 'page': page})
        # soup = BeautifulSoup(response.body, 'html.parser')
        # comments = soup.find_all('div', _class='review-short')
        # print comments

