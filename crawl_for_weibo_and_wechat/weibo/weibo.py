#!/usr/bin/env python
# -*-coding: utf-8-*-
import time
import json
import logging.config

class WeiboType(object):
    @staticmethod
    def get_from_weibo(body):
        body = json.loads(body)
        for i in body['statuses']:  
            everyone_dic = {}
            everyone_dic['published_time'] = int(
                time.mktime(time.strptime(i['created_at'].replace('+0800', ''), "%a %b %d %H:%M:%S %Y")))
            everyone_dic['tweet_id'] = i['id']
            if 'deleted' in i:  
                everyone_dic['deleted'] = 1
                everyone_dic['err_msg'] = '访问的页面地址有误，或者该页面不存在'
                yield everyone_dic
                continue
            else:
                everyone_dic['deleted'] = 0
            everyone_dic['tweet_content'] = i['text']
            if 'pic_ids' in i and 'bmiddle_pic' in i:
                for index, j in enumerate(i['pic_ids']):
                    pic_url = i['bmiddle_pic'].replace(i['bmiddle_pic'].split('/')[-1].split('.')[0], j)
                    i['pic_ids'][index] = pic_url
                everyone_dic['pic_url'] = i['pic_ids']  
                everyone_dic['video_url'] = ''
            else:
                everyone_dic['pic_url'] = []  
                if i['url_objects'] and 'info' in i['url_objects'][0] and 'url_long' in i['url_objects'][0]['info']:
                    everyone_dic['video_url'] = i['url_objects'][0]['info']['url_long']
                else:
                    everyone_dic['video_url'] = ''
            if 'retweeted_status' in i:
                everyone_dic['tweet_type'] = 2
            else:
                everyone_dic['tweet_type'] = 1  
            everyone_dic['nickname'] = i['user']['name']  
            everyone_dic['weibo_id'] = i['user']['id']  
            everyone_dic['followers_count'] = i['user']['followers_count']  
            everyone_dic['description'] = i['user']['description']  
            everyone_dic['respost_count'] = i['reposts_count']  
            everyone_dic['comment_count'] = i['comments_count']  
            everyone_dic['like_count'] = i['attitudes_count']  
            yield everyone_dic
