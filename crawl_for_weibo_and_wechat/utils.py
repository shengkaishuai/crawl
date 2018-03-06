# -*- coding: utf8 -*-
import requests
import threadpool
import logging

from weibo.crawl_from_weibo import WeiboType
from weibo import convert
from weixin.crawl_from_weixin import WeixinType

logger = logging.getLogger()

class Utils:
    @staticmethod
    def crawl(platform, url, result_list):
        if platform == '1':
            r = requests.get(url)
            for every_dic in WeiboType.weibo_crawl(r.text):
                result_list.append(every_dic)
        if platform == '9':
            r = requests.get(url)
            every_dic = WeixinType.weixin_crawl(r.text)  # 每次返回一个every_dic
            every_dic['url'] = url
            result_list.append(every_dic)

    @staticmethod
    def pool(platform, need_to_be_urls):
        # TODO 这个函数可以作为一个通用的函数，不用在里面区分平台。不要把业务的逻辑散布的到处都有。
        if platform == '1':
            result_list = []
            params = [([platform, need_to_be_urls, result_list], None)]
        elif platform == '9':
            result_list = []
            params = [([platform, url, result_list], None) for url in need_to_be_urls.split(',')[:50]]  # url是每一个url，result_list是结果存放的列表，并只处理前50

        pool = threadpool.ThreadPool(10)  # 线程池的线程数
        reqs = threadpool.makeRequests(Utils.crawl, params)  # 调用makeRequests创建了要开启多线程的函数，以及函数相关参数和回调函数，其中回调函数可以不写，default是无，也就是说makeRequests只需要2个参数就可以运行
        [pool.putRequest(req) for req in reqs]  # 把创建好的多线程丢给50个任务执行
        pool.wait()
        return platform, result_list


