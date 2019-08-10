# -*- coding: utf-8 -*-
import re
# import json
import requests

# from bs4 import BeautifulSoup
from fake_useragent import UserAgent

# 1爬取排行榜视频
# v = 0
# d = 1
# url = "https://api.bilibili.com/x/web-interface/ranking?rid={}&day={}".\format(v, d)

# 2爬取视频附属信息
# aid = 53847211
# url = "http://www.bilibili.com/video/av" + str(aid)

# 3爬取视频弹幕
# cid = 92117793
# url = "http://comment.bilibili.com/{}.xml".format(cid)

# 附加爬取UP主的投稿视频
# uid = 250858633
# size = 10
# n = 1
# url = "http://space.bilibili.com/ajax/member/getSubmitVideos?mid=" + \
#             str(uid) + "&pagesize=" + str(size) + "&page=" + str(n)

# res = requests.get(url=url,
#                    headers={"User-Agent": UserAgent().random},
#                    timeout=20)
# res.encoding = 'utf-8'
# soup = BeautifulSoup(res.text, 'lxml')

# print(soup.prettify())

# print(json.dumps(res.json, indent=2))
# print(UserAgent().random)

t = 'https://upos-hz-mirrorcosu.acgvideo.com/upgcxcode/51/07/109140751/109140751-1-30112.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1565449388&gen=playurl&os=cosu&oi=3755376044&trid=45be09b2654046198f639ab4c52bdc60p&platform=pc&upsig=e0597711f1345a4a24c5e302400b0824&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,platform&mid=45900908"],"codecs":"avc1.640028","base_url":"https://upos-hz-mirrorks3u.acgvideo.com/upgcxcode/51/07/109140751/109140751-1-30112.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1565449388&gen=playurl&os=ks3u&oi=3755376044&trid=45be09b2654046198f639ab4c52bdc60p&platform=pc&upsig=baee6ee65730e325c18e4bf43e185e48&uparams=e'
# t = 'cgvideo.com/upgcxcode/15/74/96367415/96367415_nb2-1-30011.m4s?expires=1560306900&platform=pc&ssig=wLlccL9E6Mm7qfMVU8HeFw&oi=666770708&trid=7508be6c722840a9a507c10b76b147f5&nfb=maPYqpoel5MI3qOUX6YpRA==&nfc=1&mid=45900908","http://cn-zjjh2-cmcc-v-04.acgvideo.com/upgcxcode/15/74/96367415/96367415_nb2-1-30011.m4s?expires=1560306900&platform=pc&ssig=wLlccL9E6Mm7qfMVU8HeFw&oi=666770708&trid=7508be6c722840a9a507c10b76b147f5&nfb=maPYqpoel5MI3qOUX6YpRA==&nfc=1&mid=45900908"],"bandwidth":278747,"sar":"1:1","codecs":"hev1.1.6.L120.90","base_url":"http://'
cid1 = re.search(r'/upgcxcode/(\d+)/(\d+)/(\d+)/', t).group()
cid2 = re.search(r'\d{8}', cid1).group()
cid = re.search(r'\d+', cid2).group()
print(cid2)
