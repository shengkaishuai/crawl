# -*- coding: utf-8 -*-
# author: baiyinchuan <baiyinchuan@weiboyi.com>

from __future__ import unicode_literals

import re


def validate_weixin_url(url, **kwargs):
    # https://mp.weixin.qq.com/s?src=3&timestamp=1503536401&ver=1&signature=tu7Z7dFoN0UJrPIBvihajHjA3KplU2q3bbJ-GHCeDYPq4jrutJwsTDg-lWTcKJwfbrbh1L7VI5zMFOHIhur6orI0r2ePCZd0sjWNXuwsXrkwB6y0pVq1QjuJ0do5dVUE4e5zWw7XAWd4YNwPVhdbxJ29IIznnhWw-ZsWOaX0q8g=
    # https://mp.weixin.qq.com/s?src=11&timestamp=1503536402&ver=349&signature=rlZbvcnQNeDjP3qNhE8MW4CM7u4hPGbgKKHKG7TMhQ4b0--f1M-cmeau5g6TZ4knrXlsUBeiUX2i7oaIqDNPSmmE*KGdFOvo6W4n*-mG8jwWDSSrltIZCwrHjQ65MEJ5&new=1
    # https://mp.weixin.qq.com/s?__biz=MzA4MDQ1NTAyMQ==&mid=2650279421&idx=1&sn=1c30ed8d49a1b028ee46de81f4f32d3a&chksm=87af59ffb0d8d0e99e23fcac69a0d32b0f655322336074b110ca74a79cef330d0c82b33d18e2#rd
    url_regax_1 = r'^https?://mp\.weixin\.qq\.com\/s\??.*'

    url_match_result_1 = re.match(url_regax_1, url)

    if url_match_result_1:
        return True
    else:
        return False
