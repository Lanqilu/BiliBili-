# -*- coding: utf-8 -*-
import json
import os
import re
import sys
import time
import random
import requests
import pandas
"""
该程序作用:通过排行榜中爬取的视频aid代号获取其他更多视频信息

爬取需要:
aid:视频代号

爬取得到：
cid:视频弹幕代号(之后爬取弹幕用)

关注点:
aid_change()函数
"""


"""
该程序作用:爬取弹幕池中的弹幕

爬取需要:
cid：视频弹幕编号

爬取得到:
对应视频的弹幕池中的弹幕
(弹幕池:B站会清除部分历史弹幕,弹幕池中的弹幕是会在视频播放时出现)
"""

def date():
    """
    获取现在时间格式为-年-月-日
    """
    date = time.strftime("%Y-%m-%d", time.localtime())
    return date

def get_aid():
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
    aid_dict = {}
    
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
    with open("../排行榜/{}/aid/BiliBili-{}-{}-{}.json".format(save_path, "全站", "日排行", "aid")
            ,'r', encoding='utf-8') as f1:
        aid_list = json.load(f1)  # 读取文件
        for i in aid_list:
            cid = aid_change(i)
            aid_dict[i] = cid
            print(aid_dict)
            cid_list.append(int(cid))

            # print(cid_list)
            j = j + 1
            print("{}%".format(j))
        f1.close()

    # with open("{}/BiliBili-{}-{}-cid.json".format(date(),"全站","日排行"),'w', encoding ='utf-8') as f2:
    with open("{}/BiliBili-{}-{}-cid.json".format(save_path, "全站", "日排行"),'w', encoding ='utf-8') as f2:
        json.dump(cid_list, f2)
    pandas.DataFrame(aid_dict).to_csv('aid_dict.csv')

def get_url(url, type1):
    """
    url：网站url\n
    type1：返回数据类型\n
    优化requests库中的get()函数\n
    """
    # 使用的代理ip地址
    # https://www.kuaidaili.com/free/
    # http://ip.zdaye.com/dayProxy.html
    # proxy = {"http": '117.191.11.111:8080'}
    # proxy = {"http": '47.97.82.218:8080'}
    
    ls = [{'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:22.0) Gecko/20130405 Firefox/22.0'},
          {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:14.0) Gecko/20100101 Firefox/18.0.1'},
          {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2309.372 Safari/537.36'},
          {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20130331 Firefox/21.0'}
         ]

    if type1 is None:
        res = requests.get(url=url,headers = dict(random.choice(ls)), timeout=20)
        # res = requests.get(url=url,timeout=20)
    elif type1 == "json":
        res = requests.get(url=url,headers = dict(random.choice(ls)), timeout=20).json()
        # res = requests.get(url=url, timeout=20).json()
    elif type1 == "text":
        res = requests.get(url=url,headers = dict(random.choice(ls)), timeout=20).text
        # res = requests.get(url=url, timeout=20).text
    # elif type1 == '1':
    #     res = requests.get(url=url, proxies = proxy, headers={"User-Agent": UserAgent().random}, timeout=40).text
    #     # time.sleep(random.randint(0,2))
    # elif type1 == '2':
    #     res = requests.get(url=url, proxies = proxy, headers={"User-Agent": UserAgent().random}, timeout=40).json()
    return res

    # 输出类型为json的对象，json是一种轻量级的数据交换格式
    # 易于人阅读和编写，同时也易于机器解析和生成，并有效地提升网络传输效率

def aid_change(aid):
    """
    从url中寻找cid\n
    cid:视频弹幕id\n 
    """
    url = "http://www.bilibili.com/video/av" + str(aid)
    res = get_url(url, "text")
    try:
        cid0 = re.search(r'cid=\d+', res).group()  # /d匹配数字 +重复/d
        cid = re.search(r'\d+', str(cid0)).group()  # .group()返回匹配小组字符串
    except:
        # cid1 = re.search(r'/upgcxcode/(\d+)/(\d+)/(\d+)/(\d+)-', res).group()
        # cid2 = re.search(r'/\d+-', cid1).group()
        # cid = re.search(r'\d+', cid2).group()
        cid1 = re.search(r'/upgcxcode/(\d+)/(\d+)/(\d+)/', res).group()
        cid2 = re.search(r'\d{8}', cid1).group()
        cid = re.search(r'\d+', cid2).group()
    print(cid)
    return cid

def get_danmu():
    danmu_list = []
    cid_list = []
    j = 0
    cid = 93489702
    try:
        os.chdir("./数据/视频弹幕")
    except:
        os.makedirs("./数据/视频弹幕")
        os.chdir("./数据/视频弹幕")

    save_path = date()
    if not os.path.exists(save_path):

        os.makedirs(save_path)

    with open("../排行榜/{}/BiliBili-{}-{}-cid.json".format(date(), "全站", "日排行"),
            'r',
            encoding='utf-8') as f2:
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
            res = get_url(url, None)
            res.encoding = 'utf-8'
            danmu = re.findall('">(.*?)</d>', res.text)
            j = j + 1
            print(str(j) + "%")
            # save_path = date

            with open('{}/{}.json'.format(save_path, cid), 'w',
                    encoding="utf-8") as json_file:  # 在打开模式w下修改
                for i in danmu:
                    danmu_list.append(i)
                json.dump(danmu_list, json_file, ensure_ascii=False)
                # ensure_ascii=False关闭json保存中文时使用ascii码，便于人查看
                json_file.close()
                danmu_list = []

if __name__ == "__main__":
    get_aid()
    get_danmu()
    