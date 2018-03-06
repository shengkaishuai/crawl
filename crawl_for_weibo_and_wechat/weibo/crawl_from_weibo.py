# -*- coding: utf-8 -*-
import time
import json
import urlparse
import convert

default_weibo_url = "https://c.api.weibo.com/2/statuses/show_batch/biz.json"   # 微博api网址
default_access_token = "2.00FhDfSGTxlHmCedd44e9e08s7fSVD"   # 微博接口需要的用户验证，采取默认模式

# 针对获取到的weibo内容进行字符解析
class WeiboType(object):

    @staticmethod
    # TODO 这个只是与微博有关，那就把它放到微博的模块
    def weibo_encode(need_to_be_url):
        list_of_url = []  # 获得每条微博解码的ids
        dict_url = {}  # url和每条微博对应的
        for i in need_to_be_url:  # everyone是个url，只处理前50个
            to_be_decode = urlparse.urlparse(i).path.split('/')[2]  # 拆分出来的待编码字段
            if to_be_decode.isdigit():
                decode_result_ids = to_be_decode
            else:
                decode_result_ids = convert.mid_base62_decode(to_be_decode)  # 解码的单条微博id
            dict_url[decode_result_ids] = i  # 拥有了一个带有url和每条微博对应的字典  # 注意这里不用写dict['']而写成dict[]格式，key依旧是str类型,所以后面的调用要先把获取到的str()化
            list_of_url.append(decode_result_ids)  # 获得纯数字的单条微博id列表
        list_of_url = ','.join(list_of_url)  # 将列表格式的url拼成逗号分割的形式
        url = default_weibo_url + '?' + 'access_token=' + default_access_token + '&' + 'ids=' + list_of_url  # 正常的请求的url，发向weibo api
        # print dict_url
        return url, dict_url


    @staticmethod
    def weibo_crawl(body):
        body = json.loads(body)
        for i in body['statuses']:  # 获取了每条微博的全部内容
            everyone_dic = {}
            everyone_dic['published_time'] = int(time.mktime(time.strptime(i['created_at'].replace('+0800', ''), "%a %b %d %H:%M:%S %Y")))
            everyone_dic['tweet_id'] = i['id']
            if 'deleted' in i:  # 字符串表达方式，不是json类型的字符串比如bs库形式要调用findall方法判断
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
                everyone_dic['pic_url'] = i['pic_ids']  # 这种方式把列表进行赋值 即二级赋值的方法
                everyone_dic['video_url'] = ''
            else:
                everyone_dic['pic_url'] = []  # 打印图片地址 # 如果微博是视频，变成了短地址  # 若为空，则打出空列表
                if i['url_objects'] and 'info' in i['url_objects'][0] and 'url_long' in i['url_objects'][0]['info']:
                    everyone_dic['video_url'] = i['url_objects'][0]['info']['url_long']
                else:
                    everyone_dic['video_url'] = ''
            if 'retweeted_status' in i:
                everyone_dic['tweet_type'] = 2
            else:
                everyone_dic['tweet_type'] = 1  # 判断转发还是直发
            everyone_dic['nickname'] = i['user']['name']  # user的微博名
            everyone_dic['weibo_id'] = i['user']['id']  # user的id
            everyone_dic['followers_count'] = i['user']['followers_count']  # 粉丝数
            everyone_dic['description'] = i['user']['description']  # 简介
            everyone_dic['respost_count'] = i['reposts_count']  # 转发数
            everyone_dic['comment_count'] = i['comments_count']  # 单条微博的评论量
            everyone_dic['like_count'] = i['attitudes_count']  # 单条微博的点赞量
            yield everyone_dic
