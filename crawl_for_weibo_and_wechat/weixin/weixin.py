#!/usr/bin/env python
# -*-coding: utf-8-*-
from bs4 import BeautifulSoup
import re
import time
import logging


class WeixinType(object):
    @staticmethod
    def get_from_weixin(body):

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
                video_url.append(i['data-src'])
            every_dic['video_url'] = video_url
        else:
            every_dic['video_url'] = []
        author2 = soup.find('span', class_="rich_media_meta rich_media_meta_text rich_media_meta_nickname")
        if author2:
            every_dic['author2'] = repr(author2.string).decode("unicode–escape")  # author222 一定会有，在后面
        else:
            every_dic['author2'] = ''
        all_img = soup.find_all('img', class_="")
        img_url = []
        if all_img:
            for index, every_img in enumerate(all_img): 
                img_url.append(every_img['data-src'])
            every_dic['img_url'] = img_url
       
        author_info = soup.find('div', class_="rich_media_meta_list")
        if author_info:
            time_and_author1 = author_info.find_all('em')  
            for index, j in enumerate(time_and_author1):
                if index == 0:
                   
                    every_dic['publish_time'] = int(
                        time.mktime(time.strptime(j.string.replace('+0800', ''), "%Y-%M-%S")))
                if index == 1:
                    
                    every_dic['author1'] = j.string
                else:
                    every_dic['author1'] = ''

        
        a = 'var idx = "" || "" || "1";'
        b = re.findall('var idx = "(\d)?" \|\| "(\d)?" \|\| "(\d)?";', a)
        for i in b[0]:
            if i.isdigit():
                every_dic['图文位置'] = str(i)
        
        pattern2 = re.compile(r"var msg_source_url = '(.*)';")
        msg_source_url = pattern2.findall(body)[0]
        every_dic['原文链接'] = msg_source_url.replace('\\x26', '&').replace('\r\n', '').replace('\t', '')
        content = soup.find('div', class_="rich_media_content")
        every_dic['图文内容'] = content.text.replace('\\x26', '&').replace('\r\n', '').replace('\t', '')
        return every_dic
