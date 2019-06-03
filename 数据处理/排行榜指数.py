# -*- coding: utf-8 -*-
import json
import os
import time

def date():
    """
    获取现在时间格式为-年-月-日
    """
    date = time.strftime("%Y-%m-%d", time.localtime())
    return date



date_list = []
index_list = []
for i in range(1,101):
    index_list.append(i) 
title_list = []
play_list = []
coins_list = []
pts_list = []
coins_play_list = []

date_type = ['title', 'play', 'coins', 'pts']
for k in date_type:
    with open("./数据/排行榜/{}/{}/BiliBili-{}-{}-{}.json".format(date(), k, "全站", "日排行", k), 'r', encoding='utf-8') as date1:
        date_list = json.load(date1) # 读取文件
        for i in date_list:
            if k == 'title':
                title_list.append(i)
            elif k == 'play':
                play_list.append(i)
            elif k == 'coins':
                coins_list.append(i)
            else:
                pts_list.append(i)
# print(play_list)
# print(coins_list)

pts_dict = dict(zip(title_list, pts_list))

for i, j in zip(play_list, coins_list):
        x = (j/i)*100
        # print(i)
        coins_play_list.append(x)
coins_dict = dict(zip(title_list, coins_play_list))

save_path = date()
os.chdir("./数据处理结果")# 切换工作目录
if not os.path.exists(save_path):
    os.makedirs(save_path)

with open("{}/BiliBili-{}.json".format(save_path,'pts_dict'), 'w', encoding='utf-8')as date2:
    json.dump(pts_dict, date2, ensure_ascii=False)
with open("{}/BiliBili-{}.json".format(save_path,'coins_dict'), 'w', encoding='utf-8')as date3:
    json.dump(coins_dict, date3, ensure_ascii=False)
with open("{}/BiliBili-{}.json".format(save_path,'coins_list'), 'w', encoding='utf-8')as date4:
    json.dump(coins_list, date4, ensure_ascii=False)


# print(pts_dict)
# print(coins_dict)


