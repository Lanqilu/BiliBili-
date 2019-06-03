# -*- coding: utf-8 -*-
import json
import requests

from bs4 import BeautifulSoup
from fake_useragent import UserAgent

# 1爬取排行榜视频
# v = 0
# d = 1
# url = "https://api.bilibili.com/x/web-interface/ranking?rid={}&day={}".format(v, d)

# 2爬取视频附属信息
# aid = 53847211
# url = "http://www.bilibili.com/video/av" + str(aid)


# 3爬取视频弹幕
# cid = 92117793
# url = "http://comment.bilibili.com/{}.xml".format(cid)

# 附加爬取UP主的投稿视频
uid = 250858633
size = 10
n = 1
url = "http://space.bilibili.com/ajax/member/getSubmitVideos?mid=" + \
            str(uid) + "&pagesize=" + str(size) + "&page=" + str(n)

res = requests.get(url=url, headers={"User-Agent": UserAgent().random}, timeout=20)
res.encoding = 'utf-8'
soup = BeautifulSoup(res.text, 'lxml')

print(soup.prettify())

# print(json.dumps(res.json, indent=2))
