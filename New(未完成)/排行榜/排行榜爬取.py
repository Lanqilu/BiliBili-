# -*- coding: utf-8 -*-
import json
import sys
import os
import time
import random
import requests
import pandas
"""
该程序作用:
爬取各区的排行榜名单
爬取得到：
    aid:视频代号
    coins:视频受到的硬币数
    (硬币是B站用户每日登录时获得的一种虚拟物品，每日每人一个，对一个稿件每人最多投两个硬币，反映对视频的喜爱程度)
    paly:视频播放数
    (这个播放数是排行榜的播放数，而不是视频总播放数)
    (例如一个日排行榜爬出来播放数1万，可能实际总播放数有3万，而这个1万是指排行榜更新前这1日的播放数)
    (同理三日、周、月分别指的是三日、周、月的播放数)
    pts:B站按一定公式计算出是综合得分
    title:视频标题
"""

def date():
    """
    获取现在时间格式为-年-月-日
    """
    date = time.strftime("%Y-%m-%d", time.localtime())
    return date

def print_info(j):
    """
    打印进程
    """
    r = j / 52
    list1 = []
    for i in range(1, 101):
        list1.append(i)
    if r in list1:
        print("{}%".format(r))
    elif r == 100:
        print("成功完成")

class ShowProcess():
    """
    显示处理进度的类
    调用该类相关函数即可实现处理进度的显示
    """
    i = 0 # 当前的处理进度
    max_steps = 0 # 总共需要处理的次数
    max_arrow = 50 #进度条的长度
    infoDone = 'Done'

    # 初始化函数，需要知道总共的处理次数
    def __init__(self, max_steps, infoDone = 'Done'):
        self.max_steps = max_steps
        self.i = 0
        self.infoDone = infoDone

    # 显示函数，根据当前的处理进度i显示进度
    # 效果为[>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>]100.00%
    def show_process(self, i=None):
        if i is not None:
            self.i = i
        else:
            self.i += 1
        num_arrow = int(self.i * self.max_arrow / self.max_steps) #计算显示多少个'>'
        num_line = self.max_arrow - num_arrow #计算显示多少个'-'
        percent = self.i * 100.0 / self.max_steps #计算完成进度，格式为xx.xx%
        process_bar = '[' + '>' * num_arrow + '-' * num_line + ']'\
                      + '%.2f' % percent + '%' + '\r' #带输出的字符串，'\r'表示不换行回到最左边
        sys.stdout.write(process_bar) #这两句打印字符到终端
        sys.stdout.flush()
        if self.i >= self.max_steps:
            self.close()

    def close(self):
        print('')
        print(self.infoDone)
        self.i = 0

def get_value(dict_name, object_key):
    """
    从嵌套的字典中找到需要的值\n
    dict_name: 要查询的字典\n
    object_key: 目标key\n
    返回目标key对应的value\n
    """
    if isinstance(dict_name, dict):
        # isinstance()函数来判断一个对象是否是一个已知的类型，类似type()优于type() P17
        for key, value in dict_name.items():
            if key == object_key:
                return value
            else:
                # 如果value是dict类型，采用递归
                if isinstance(value, dict):
                    ret = get_value(value, object_key)
                    if ret is not None:
                        return ret
                # 如果value是list类型，则依次进行递归
                elif isinstance(value, list):
                    for i in range(len(value)):
                        ret = get_value(value[i], object_key)
                        if ret is not None:
                            return ret
        # 如果找不到指定的key，返回None
        return None
    else:
        return None

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
 

def leaderboard():
    ''' 爬取B站现在各个分区的日排行、三日排行、周排行、月排行 '''
    os.chdir("./数据/排行榜")  # 切换工作目录
    """
    VC code 的相对目录和其他IDE有不同，貌似是工作区的原因
    VC code的./是打开的主文件夹的下的路径
    PyCharm,IELD以运行文件的文件夹的路径为./
    如果要在PyCharm,IELD下调试需要把部分./改为../
    """
    save_path = date()  # 爬取结果的文件保存目录

    # 各项数据存储列表
    aid_list = []
    coins_list = []
    play_list = []
    pts_list = []
    title_list = []
    uid_list = []

    date_type = ['aid', 'coins', 'play', 'pts', 'title', 'uid']
    """
    date_type 相关值说明
    aid:视频代号
    coins:视频受到的硬币数
    (硬币是B站用户每日登录时获得的一种虚拟物品，每日每人一个，对一个稿件每人最多投两个硬币，反映对视频的喜爱程度)
    paly:视频播放数
    pts:B站按一定公式计算出是综合得分
    title:视频标题
    """

    # 如果文件名称重复则将旧文件夹重命名以尾部加0开始依次递推,防止文件夹重复
    if os.path.exists(save_path):
        try:
            os.rename(save_path, save_path + "0")
        except FileExistsError:
            i = 0
            while os.path.exists(save_path + str(i)):
                i = i + 1
                continue
            os.rename(save_path, save_path + str(i))

    os.makedirs(save_path + '\\' + '结果')
    # 循环创建子目录
    for fl in date_type:
        os.makedirs(save_path + '\\' + str(fl))

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
    # 排行榜时间范围字典,对应url的day=值
    day_dict = {"日排行": 1, "三日排行": 3, "周排行": 7, "月排行": 30}
    
    for k1, v in area_dict.items():
        for k2, d in day_dict.items():
            with open("{}/结果/BiliBili-{}-{}.csv".format(save_path, k1, k2),"a",
                        encoding="utf-8") as data_file2:
                data_file2.write("title,author,uid,aid,play,coins,pts\n")
            

    # for循环将分区字典的值分次分别写入到k1和v
    for k1, v in area_dict.items():  # items()返回字典中所有的一一对应的值
        # for循环排行时间字典
        for k2, d in day_dict.items():
            # B站排行榜API的url 修改rid=可以改变分区，修改day=可以改变排行榜时间范围
            url = "https://api.bilibili.com/x/web-interface/ranking?rid={}&day={}".format(v, d)
            res = get_url(url, "json")
            # 输出类型为json的对象，json是一种轻量级的数据交换格式

            # 必要时检查res是否有错误
            # print(json.dumps(res, indent=2))
            # break

            # 也可以采用正则表达式进行数据匹配，例如下面
            # res = get_url(url,'text')
            # aid = re.findall(r'"aid":"\d+",',res)

            # 但受到网友启发，发现像这种api保存到python中正好是字典类型
            # 通过处理，相较于正则表达式有着更好的一条条数据对应起来
            # 在逻辑有上更条理
            # 并且在爬取其他类似api接口时可以适当修改使用
            # 详见function/deal_fuc.py的get_value函数
            rank_list = get_value(res, "list")

            for i in range(len(rank_list)):
                aid0 = get_value(rank_list[i], "aid")  # 视频aid
                author0 = get_value(rank_list[i], "author")  # up主
                coins0 = get_value(rank_list[i], "coins")  # 投币数
                play0 = get_value(rank_list[i], "play")  # 播放数
                pts0 = get_value(rank_list[i], "pts")  # 综合得分
                title0 = get_value(rank_list[i], "title")  # 视频标题
                uid0 = get_value(rank_list[i], "mid")  # UP主代号

                # 将数据保存为列表
                aid_list.append(int(aid0))
                coins_list.append(int(coins0))
                play_list.append(int(play0))
                pts_list.append(int(pts0))
                title_list.append(title0)
                uid_list.append(int(uid0))

                for k3 in date_type:
                    with open("{}/{}/BiliBili-{}-{}-{}.json".format(save_path, k3, k1, k2, k3),                              "w",
                              encoding="utf-8") as json_file:
                        json.dump(eval("{}_list".format(k3)),json_file,ensure_ascii=False)
                        # eval()将字符串str当成有效的表达式来求值并返回计算结果
                        json_file.close()

                # 将数据保存为txt文件
                with open("{}/结果/BiliBili-{}-{}.txt".format(save_path, k1, k2),"a",
                          encoding="utf-8") as data_file:
                    data_file.write("排名: {}\n".format(i + 1))
                    data_file.write("投币数: {}\n".format(coins0))
                    data_file.write("播放数: {}\n".format(play0))
                    data_file.write("视频aid: {}\n".format(aid0))
                    data_file.write("综合得分: {}\n".format(pts0))
                    data_file.write("UP主: {}\n".format(author0))
                    data_file.write("视频标题: {}\n".format(title0))
                    data_file.write("*" * 70 + "\n")
                    data_file.close()
                with open("{}/结果/BiliBili-{}-{}.csv".format(save_path, k1, k2),"a",
                          encoding="utf-8") as data_file2:
                    data_file2.write("{},{},{},{},{},{},{}\n".format(title0,author0,uid0,aid0,play0,coins0,pts0))
       
                # # 显示打印进程
                process_bar.show_process()
                time.sleep(0.001)
            # 一次循环后清空列表
            aid_list = []
            coins_list = []
            play_list = []
            pts_list = []
            title_list = []
if __name__ == "__main__":
    # 当.py文件被直接运行时，if __name__ == '__main__'之下的代码块将被运行；
    # 当.py文件以模块形式被导入时，if __name__ == '__main__'之下的代码块不被运行。
    max_steps = 5200   # 总共需要处理的次数
    process_bar = ShowProcess(max_steps, '完成')
    leaderboard()