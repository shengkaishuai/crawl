#!/usr/bin/env python
# -*-coding: utf-8-*-
import logging
from urllib2 import urlparse

import requests
import threadpool

from weibo import WeiboType, convert
from weixin.weixin import WeixinType

logger = logging.getLogger()

default_weibo_url = "https://c.api.weibo.com/2/statuses/show_batch/biz.json"   # 微博api网址
default_access_token = "2.00*******HmCedd44e9e08s7fSVD"   # 微博接口需要的用户验证，一般需要购买

class Outter:
    @staticmethod
    def crawl(platform, url, result_list):
        if platform == '1':
            try:
                r = requests.get(url)
                for every_dic in WeiboType.get_from_weibo(r.text):
                    result_list.append(every_dic)
            except:
                logger.error('Error : need params of platform or urls')
        if platform == '9':
            r = requests.get(url)
            every_dic = WeixinType.get_from_weixin(r.text)  # 每次返回一个every_dic
            every_dic['url'] = url
            result_list.append(every_dic)
    @staticmethod
    def pool(platform, need_to_be_urls):
        if platform == '1':
            result_list = []
            params = [([platform, need_to_be_urls, result_list], None)]
        elif platform == '9':
            result_list = []
            params = [([platform, url, result_list], None) for url in need_to_be_urls.split(',')[:50]]  

        pool = threadpool.ThreadPool(10)  
        reqs = threadpool.makeRequests(Outter.crawl, params)  
        [pool.putRequest(req) for req in reqs]  
        pool.wait()
        return platform, result_list


    @staticmethod
    def weibo_encode(need_to_be_url):
        list_of_url = []  
        dict_url = {}  
        for i in need_to_be_url:  
            to_be_decode = urlparse.urlparse(i).path.split('/')[2]  
            if to_be_decode.isdigit():
                decode_result_ids = to_be_decode
            else:
                decode_result_ids = convert.mid_base62_decode(to_be_decode)  
            dict_url[decode_result_ids] = i  
            list_of_url.append(decode_result_ids)  
        list_of_url = (',').join(list_of_url)  
        url = default_weibo_url + '?' + 'access_token=' + default_access_token + '&' + 'ids=' + list_of_url  
        return url, dict_url