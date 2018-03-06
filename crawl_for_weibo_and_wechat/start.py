#!/usr/bin/env python
# -*-coding: utf-8-*-
import json
import time

import tornado.gen
import tornado.httpclient
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options

from outter import *
from weibo import weibo_validator
from weixin import weixin_validator

define("port", default=8080, help="run on the given port", type=int)
logger = logging.getLogger()

CODE_MAP = {'1000': {'code': 1000, 'err_msg': '', 'user': {}},
            '1001': {'code': 1001, 'err_msg': '缺少参数', 'user': {}},
            '1002': {'code': 1002, 'err_msg': '该资源平台暂不支持', 'user': {}},
            '1003': {'code': 1003, 'err_msg': '系统抓取错误', 'user': {}},
            '1004': {'code': 1004, 'err_msg': '账号不存在', 'user': {}},
            '1005': {'code': 1005, 'err_msg': '抓取参数格式错误', 'user': {}},
            '1006': {'code': 1006, 'err_msg': '其他错误', 'user': {}}
            }

class IndexHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        # try:
        time1 = time.time()
        platform = self.get_argument('weibo_type').encode('utf-8')
        need_to_be_urls = self.get_argument('urls')  # need_to_be_url是个字符串
        print "need_to_be_url:", need_to_be_urls

        correct_http = []
        error_http = []
        if platform == '1':
            for i in need_to_be_urls.split(',')[:50]:
                if weibo_validator.validate_weibo_url(i):
                    correct_http.append(i)
                else:
                    error_http.append(i)
            need_to_be_urls, dict_url = Outter.weibo_encode(correct_http)  
            platform, result_list = Outter.pool(platform, need_to_be_urls)  
            for i in result_list:  
                i['url'] = dict_url[str(i['tweet_id'])]  
            for i in error_http:
                error_dict = {}
                error_dict['err_msg'] = 'http网址错误'
                error_dict['url'] = i
                result_list.append(error_dict)
        elif platform == '9':
            for i in need_to_be_urls.split(',')[:50]:
                if weixin_validator.validate_weixin_url(i):
                    correct_http.append(i)
                else:
                    error_http.append(i)
            need_to_be_urls = (',').join(correct_http)
            platform, result_list = Outter.pool(platform, need_to_be_urls)  
            for i in error_http:
                error_dict = {}
                error_dict['err_msg'] = 'http网址错误'
                error_dict['url'] = i
                result_list.append(error_dict)


        CODE_MAP['1000']['user'] = result_list



        if result_list:
            result = CODE_MAP['1000']
            logger.info('successfully present the result')
            result = json.dumps(result)
            self.write(result)
        else:
            result = CODE_MAP['1003']
            logger.info('系统抓取错误')
            result = json.dumps(result)
            self.write(result)
            self.finish()
        time2 = time.time()
        print time2 - time1



if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r"/crawldata", IndexHandler)])  
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


