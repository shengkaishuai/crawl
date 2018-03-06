# -*- coding: utf-8 -*-
# author: baiyinchuan <baiyinchuan@weiboyi.com>

from __future__ import unicode_literals

import re


def validate_weibo_url(url, **kwargs):
    # http://weibo.com/1984563793/F3Eaw89YU?ref=home&rid=11_0_8_2778213081640564544&type=comment
    # http://m.weibo.cn/status/4102514783180645
    # https://m.weibo.cn/status/F3Eaw89YU
    # https://weibo.cn/6079558461/F3zu2whZc?type=comment
    # http://www.weibo.com/2649521297/F2kAflgxm?from=page_1005052649521297_profile&wvr=6&mod=weibotime&type=comment#_rnd1495073362559
    # https://m.weibo.cn/6174448636/4105796030075794
    url_regax_1 = r'^https?://(www\.)?weibo\.com/\d+/\w+?.*'
    url_regax_2 = r'^https?://m\.weibo\.cn/status/\w+?.*'
    url_regax_3 = r'^https?://(m\.)?weibo\.cn/\d+/\w+?.*'

    url_match_result_1 = re.match(url_regax_1, url)
    url_match_result_2 = re.match(url_regax_2, url)
    url_match_result_3 = re.match(url_regax_3, url)

    if url_match_result_1 or url_match_result_2 or url_match_result_3:
        return True
    else:
        return False


if __name__ == '__main__':
    url_1 = 'http://weibo.com/1984563793/F3Eaw89YU?ref=home&rid=11_0_8_2778213081640564544&type=comment'
    url_2 = 'http://m.weibo.cn/status/4102514783180645'
    url_3 = 'https://weibo.cn/6079558461/F3zu2whZc?type=comment'
    url_4 = 'http://www.weibo.com/2649521297/F2kAflgxm?from=page_1005052649521297_profile&wvr=6&mod=weibotime&type=comment#_rnd1495073362559'
    url_5 = 'https://m.weibo.cn/status/4109176055671942?sourceType=qq&from=1075195010&wm=20005_0002'

    print validate_weibo_url(url_1)
    print validate_weibo_url(url_2)
    print validate_weibo_url(url_3)
    print validate_weibo_url(url_4)
    print validate_weibo_url(url_5)
