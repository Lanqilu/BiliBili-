# -*- coding: utf-8 -*-
"""
此程序是将排行榜的线从up投稿方向拓宽成面
加上时间轴便是有三个维度的信息
由于B站的反爬虫机制导致IP屡次被封
IP代理中免费IP偶尔能找到可以用的
由于精力原因暂时未能进行拓展
"""

import json
import os
import re

from functions.date_fuc import date
from functions.get_url_fuc import get_url

try :
    os.chdir("./数据/UP主视频")
except :
    os.makedirs("./数据/UP主视频")
    os.chdir("./数据/UP主视频")

save_path = date()
if not os.path.exists(save_path):
    os.makedirs(save_path)

# 获取指定UP的所有视频的aid号 uid:UP主代号 s:视频数量 
def get_video_list(uid, s = 10):
    """获取UP主视频列表"""
    # 视频aid号列表
    aid_list1 = []
    url = "http://space.bilibili.com/ajax/member/getSubmitVideos?mid=" + \
        str(uid) + "&pagesize=" + str(s) + "&page=1" 
    res = get_url(url,"1")  #获取url内容

    match1 = re.findall(r'"aid":[0-9]\d+', res)
    # print(match1)
    match2 = re.findall(r'[0-9]\d+', str(match1))
    print(match2)
    with open('{}/{}的视频列表.json'.format(date(), uid), 'a', encoding="utf-8") as json_file: #在打开模式a下修改
        for i in match2 :
            aid_list1.append(int(i))
        json.dump(aid_list1, json_file, ensure_ascii=False)


if __name__ == "__main__":
    j = 0
    with open ("../排行榜/{}/uid/BiliBili-全站-日排行-uid.json".format(date()), 'r', encoding='utf-8')as f1:
        up_list = json.load(f1)
        for uid in up_list:
            get_video_list(uid)
            j = j+1
            print("{}%".format(j))
        f1.close()
    print('100%')
