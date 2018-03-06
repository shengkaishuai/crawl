# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re
import time
import logging


class WeixinType(object):
    @staticmethod
    def weixin_crawl(body):

        every_dic = {}
        soup = BeautifulSoup(body, 'html.parser')
        # 获取title
        title = soup.find('title').string
        if not title:
            every_dic['err_msg'] = '页面过期或系统出错'
            return every_dic
        every_dic['title'] = title

        # audio_url链接
        audio_url = []
        mpvoice = soup.find_all('mpvoice')
        if mpvoice:
            for index, i in enumerate(mpvoice):
                url = "https://res.wx.qq.com/voice/getvoice?mediaid=" + i['voice_encode_fileid']  # 获取每一个音频的IP
                audio_url.append(url)
            every_dic['audio_url'] = audio_url
        else:
            every_dic['audio_url'] = []
        # video_url链接
        video_url = []
        video = soup.find_all('iframe', class_="video_iframe")
        if video:
            for index, i in enumerate(video):
                # print i['data-src']  # 此处加断点，发现可以用中括号[]形式取出该数  #  获取每一个视频的url
                video_url.append(i['data-src'])
            every_dic['video_url'] = video_url
        else:
            every_dic['video_url'] = []
        # 后面的作者信息
        author2 = soup.find('span', class_="rich_media_meta rich_media_meta_text rich_media_meta_nickname")
        if author2:
            every_dic['author2'] = repr(author2.string).decode("unicode–escape")  # author222 一定会有，在后面
        else:
            every_dic['author2'] = ''
        # pic_url信息
        all_img = soup.find_all('img', class_="")
        img_url = []
        if all_img:
            for index, every_img in enumerate(all_img):
                # print every_img['data-src']  # 打出每一张图片的url
                img_url.append(every_img['data-src'])
            every_dic['img_url'] = img_url
        # publish_time 和 前面的作者信息
        author_info = soup.find('div', class_="rich_media_meta_list")
        if author_info:
            time_and_author1 = author_info.find_all('em')  # find_all继续在小范围find_all 策略：两次find_all
            for index, j in enumerate(time_and_author1):
                if index == 0:
                    # print j.string  # po微信的时间
                    every_dic['publish_time'] = int(
                        time.mktime(time.strptime(j.string.replace('+0800', ''), "%Y-%M-%S")))
                if index == 1:
                    # print j.string  # 微信的第一个名字
                    every_dic['author1'] = j.string
                else:
                    every_dic['author1'] = ''

        # var idx = "" || "" || "1"; # 如果url失效，正则的每个方法都会报错，因为原html代码全部失效
        # var idx = "5" || "" || ""; 这种情况也要考虑
        # a = 'var idx = "" || "" || "1";'
        # b = re.findall('var idx = "(\d)?" \|\| "(\d)?" \|\| "(\d)?";', a)
        pattern1 = re.compile('var idx = "(\d)?" \|\| "(\d)?" \|\| "(\d)?";')
        location = pattern1.findall(body)
        for i in location[0]:
            if i.isdigit():
                every_dic['图文位置'] = str(i)
        # 原文链接
        # var msg_source_url = '';
        pattern2 = re.compile(r"var msg_source_url = '(.*)';")
        msg_source_url = pattern2.findall(body)[0]
        every_dic['原文链接'] = msg_source_url.replace('\\x26', '&').replace('\r\n', '').replace('\t', '')
        content = soup.find('div', class_="rich_media_content")
        every_dic['图文内容'] = content.text.replace('\\x26', '&').replace('\r\n', '').replace('\t', '')
        return every_dic
