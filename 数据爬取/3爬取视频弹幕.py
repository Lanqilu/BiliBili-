# -*- coding: utf-8 -*-
"""
该程序作用:爬取弹幕池中的弹幕

爬取需要:
cid：视频弹幕编号

爬取得到:
对应视频的弹幕池中的弹幕
(弹幕池:B站会清除部分历史弹幕,弹幕池中的弹幕是会在视频播放时出现)
"""
import json
import os
import re
import sys

from functions.date_fuc import date
from functions.get_url_fuc import get_url

danmu_list = []
cid_list = []
j = 0
# cid = 93489702
try :
    os.chdir("./数据/视频弹幕")
except :
    os.makedirs("./数据/视频弹幕")
    os.chdir("./数据/视频弹幕")
    
save_path = date()
if not os.path.exists(save_path):

    os.makedirs(save_path)

with open("../排行榜/{}/BiliBili-{}-{}-cid.json".format(date(), "全站", "日排行"), 'r', encoding='utf-8') as f2:
    cid_list = json.load(f2)
    print(cid_list)
    f2.close()
    for cid in cid_list:

        url = "http://comment.bilibili.com/{}.xml".format(cid)
        # 备用api接口
        # url = "https://api.bilibili.com/x/v1/dm/list.so?oid={}".format(cid)
        # 查看历史弹幕api接口
        # date = input('年-月-日')
        # https://api.bilibili.com/x/v2/dm/history?type=1&date=2019-05-29&oid=93489702
        res = get_url(url,None)
        res.encoding = 'utf-8'
        danmu = re.findall('">(.*?)</d>', res.text)
        j = j + 1
        print(str(j)+"%")
        # save_path = date

        with open('{}/{}.json'.format(save_path, cid), 'w', encoding="utf-8") as json_file: # 在打开模式w下修改
            for i in danmu:
                danmu_list.append(i)
            json.dump(danmu_list, json_file, ensure_ascii=False)
            # ensure_ascii=False关闭json保存中文时使用ascii码，便于人查看
            json_file.close()
            danmu_list = []

