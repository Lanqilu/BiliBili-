# -*- coding: utf-8 -*-
"""
该程序作用:通过排行榜中爬取的视频aid代号获取其他更多视频信息

爬取需要:
aid:视频代号

爬取得到：
cid:视频弹幕代号(之后爬取弹幕用)

关注点:
aid_change()函数
"""

import json
import os

from functions.date_fuc import date
from functions.get_url_fuc import aid_change

save_path = date()
os.chdir("./数据/排行榜")  # 切换工作目录
if not os.path.exists(save_path):
    os.makedirs(save_path)
# print(os.getcwd())uid:视频投稿者代号

area_dict = {
    "全站": 0,
    "动画": 1,
    "国创相关": 168,
    "音乐": 3,
    "舞蹈": 129,
    "游戏": 4,
    "科技": 36,
    "数码": 188,
    "生活": 160,
    "鬼畜": 119,
    "时尚": 155,
    "娱乐": 5,
    "影视": 181
}
day_dict = {"日排行": 1, "三日排行": 3, "周排行": 7, "月排行": 30}

aid_list = []
cid_list = []

j = 0

# date = input('XXXX-XX-XX')
# save_path = date
"""
启用这两段代码可以输出指定日期的排行榜视频附属信息
前提是排行榜中存在指定日期文件
"""

# for k1 in area_dict.items():
#     for k2 in day_dict.items():
# 全部爬取较费时间，多线程还不太会故以全站日排行为例
with open("../排行榜/{}/aid/BiliBili-{}-{}-{}.json".format(
        save_path, "全站", "日排行", "aid"),
          'r',
          encoding='utf-8') as f1:
    aid_list = json.load(f1)  # 读取文件
    for i in aid_list:
        cid = aid_change(i)

        cid_list.append(int(cid))

        # print(cid_list)
        j = j + 1
        print("{}%".format(j))
    f1.close()

# with open("{}/BiliBili-{}-{}-cid.json".format(date(),"全站","日排行"),'w', encoding='utf-8') as f2:
with open("{}/BiliBili-{}-{}-cid.json".format(save_path, "全站", "日排行"),'w', encoding='utf-8') as f2:
    json.dump(cid_list, f2)
