# -*- coding: utf-8 -*-

# from scrapy.conf import settings
# import pymongo
# class DoubanspiderPipeline(object):
#     def __init__(self):
#         port = settings['MONGODB_PORT']
#         host = settings['MONGODB_HOST']
#         db_name = settings['MONGODB_DBNAME']
#         client = pymongo.MongoClient(host=host, port=port)
#         db = client[db_name]
#         self.post = db[settings['MONGODB_DOCNAME']]
#
#
#     def process_item(self, item, spider):
#         book_info = dict(item)
#         self.post.insert(book_info)
#         return item


from items import *
class DoubanspiderPipeline(object):


    def process_item(self, item, spider):
        if isinstance(item, DoubanspiderItem):
            with open('try', 'a') as f:
                f.write(item['bookid'] + '\n')
                f.write(item['comment'] + '\n')
            return item
        elif isinstance(item, BookinfoItem):
            with open('bookinfo1', 'a') as f:
                f.write(item['bookname'] + '\n')
                f.write(item['bookinfo'] + '\n')
                f.write(item['bookid'] + '\n')
                f.write(item['img'] + '\n')
                f.write('\n\n\n')
            return item
