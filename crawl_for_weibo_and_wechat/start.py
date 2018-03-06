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

from utils import *
# TODO 尽量不要import *, 写出具体要导入的，避免命名冲突
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
        time1 = time.time()
        platform = self.get_argument('weibo_type').encode('utf-8')
        need_to_be_urls = self.get_argument('urls')  # need_to_be_url是个字符串

        # TODO 变量名起的有点不恰当，corrent_http里面放的是url，那为什么不起名为legal_urls_list
        correct_http = []
        error_http = []
        result_list = []
        if platform == '1':
            for i in need_to_be_urls.split(',')[:50]:
                if weibo_validator.validate_weibo_url(i):
                    correct_http.append(i)
                else:
                    error_http.append(i)
            # TODO need_to_be_urls, dict_url 让人看了根本就不知道里面放的是什么
            need_to_be_urls, dict_url = WeiboType.weibo_encode(correct_http)  # 得到dict_url  # 返回值need_to_be_url是字符串
            # print "api:" + need_to_be_url  # 这里没有问题
            platform, result_list = Utils.pool(platform, need_to_be_urls)  # result_list = pool(platform,need_to_be_url) 这样写返回结果会以元祖形式存在result_list
            for i in result_list:  # 每个i是正确结果的weibo字典
                i['url'] = dict_url[str(i['tweet_id'])]  # 把url加进字典
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
            platform, result_list = Utils.pool(platform, need_to_be_urls)  # result_list = pool(platform,need_to_be_url) 这样写返回结果会以元祖形式存在result_list
            for i in error_http:
                error_dict = {}
                error_dict['err_msg'] = 'http网址错误'
                error_dict['url'] = i
                result_list.append(error_dict)


        result = json.dumps(result_list)
        self.write(result)
        self.finish()


        time2 = time.time()
        print time2 - time1



if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r"/weiboyi/azkaban/url_data", IndexHandler)])  # 注意路径问题，一定要写全！！！
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


