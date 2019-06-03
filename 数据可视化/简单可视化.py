# -*- coding: utf-8 -*-

import os
import json
import time
import matplotlib.pyplot as plt

def date():
    """
    获取现在时间格式为-年-月-日
    """
    date = time.strftime("%Y-%m-%d", time.localtime())
    return date

save_path = date()

title_list = []
coins_list = []
pts_list = []


with open("./数据处理结果/{}/BiliBili-{}.json".format(save_path, 'coins_dict'), 'r', encoding='utf-8')as date1:
    coins_dict = json.load(date1)
    for k in coins_dict.values():
        coins_list.append(k)

with open("./数据/排行榜/{}/pts/BiliBili-全站-日排行-pts.json".format(save_path), 'r', encoding='utf-8')as date2:
    pts_list = json.load(date2)

with open("./数据/排行榜/{}/play/BiliBili-全站-日排行-play.json".format(save_path), 'r', encoding='utf-8')as date3:
    play_list = json.load(date3)

index_list = []
for i in range(1,101):
    index_list.append(i) 


os.chdir('./可视化结果')
if not os.path.exists(save_path):
    os.makedirs(save_path)


plt.figure(1)    
plt.bar(index_list, coins_list, color='m')   # 绘图类型
plt.title("Coins")    # 标题
plt.ylabel('Coins')   # y轴
plt.xlabel('Ranking') # x轴
plt.savefig("{}/Coins.png".format(save_path))# 保存到本地


plt.figure(2)    
plt.bar(index_list, play_list, color='c')
plt.title("Play")   
plt.ylabel('Play') 
plt.xlabel('Ranking') 
plt.savefig("{}/Play.png".format(save_path))

plt.figure(3)    
plt.bar(index_list, coins_list, color='c')
plt.title("Play and Coins Relationship") 
plt.ylabel('Relationship/%') 
plt.xlabel('Ranking') 
plt.savefig("{}/Play and Coins Relationship.png".format(save_path))

plt.figure(4)    
plt.bar(index_list, pts_list, color='g')
plt.plot(index_list, pts_list, color='r')
plt.title("Pts") 
plt.ylabel('Pts') 
plt.xlabel('Ranking') 
plt.savefig("{}/Pts_Ranking.png".format(save_path))

plt.figure(5)    
plt.scatter(coins_list, pts_list)
plt.title("Pts and Coins Relationship") 
plt.ylabel('Pts') 
plt.xlabel('Coins') 
plt.savefig("{}/Pts_Coins.png".format(save_path))

plt.show()