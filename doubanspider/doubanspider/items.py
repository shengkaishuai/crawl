# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    comment = scrapy.Field()
    bookid = scrapy.Field()


class BookinfoItem(scrapy.Item):
    bookid = scrapy.Field()
    bookname = scrapy.Field()
    bookinfo = scrapy.Field()
    img = scrapy.Field()