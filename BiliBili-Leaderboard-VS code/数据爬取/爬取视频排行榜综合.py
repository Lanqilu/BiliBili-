import json
import os
import re
import sys
import time

import requests
# from fake_useragent import UserAgent  # UserAgent用户代理,识别浏览器的一串字符串


# 用于处理时间
def date():
    """
    获取现在时间格式为-年-月-日
    """
    date = time.strftime("%Y-%m-%d", time.localtime())
    return date

# 打印进度条
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

# 处理嵌套数据
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

# 获取网页
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
    if type1 is None:
        #  res = requests.get(url=url, headers={"User-Agent": UserAgent().random},timeout=20)
        res = requests.get(url=url, timeout=20)
    elif type1 == "json":
        # res = requests.get(url=url, headers={"User-Agent": UserAgent().random}, timeout=20).json()
        res = requests.get(url=url, timeout=20).json()
    elif type1 == "text":
        # res = requests.get(url=url, headers={"User-Agent": UserAgent().random}, timeout=20).text
        res = requests.get(url=url, timeout=20).text
    elif type1 == '1':
        res = requests.get(url=url, proxies = proxy, headers={"User-Agent": UserAgent().random}, timeout=40).text
        # time.sleep(random.randint(0,2))
    elif type1 == '2':
        res = requests.get(url=url, proxies = proxy, headers={"User-Agent": UserAgent().random}, timeout=40).json()
    return res

    # 输出类型为json的对象，json是一种轻量级的数据交换格式
    # 易于人阅读和编写，同时也易于机器解析和生成，并有效地提升网络传输效率
 
# 由aid获取cid
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

# 获取排行榜数据并保存
def leaderboard():
    ''' 爬取B站现在各个分区的日排行、三日排行、周排行、月排行 '''
    os.chdir("./数据/排行榜")  # 切换工作目录
    """
    VC code 的相对目录和其他IDE有不同，貌似是工作区的原因
    VC code的./是打开的主文件夹的下的路径
    PyCharm,IELD以运行文件的文件夹的路径为./
    如果要在PyCharm,IELD下调试需要把部分./改为../
    """

    j = 0  # 统计循环次数,用于显示爬取进程

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

    os.makedirs(save_path + '\\' + '结果展示')
    # 循环创建子目录
    for fl in date_type:
        os.makedirs(save_path + '\\' + str(fl))

    # B站不同分区字典,对应url的rid=值
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
                    with open("{}/{}/BiliBili-{}-{}-{}.json".format(
                            save_path, k3, k1, k2, k3),
                              "w",
                              encoding="utf-8") as json_file:
                        json.dump(eval("{}_list".format(k3)),
                                  json_file,
                                  ensure_ascii=False)
                        # eval()将字符串str当成有效的表达式来求值并返回计算结果
                        json_file.close()

                # 将数据保存为txt文件
                with open("{}/结果展示/BiliBili-{}-{}.txt".format(
                        save_path, k1, k2),
                          "a",
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

                # 显示打印进程
                j = j + 1
                # print(j)
                print_info(j)
            # 一次循环后清空列表
            aid_list = []
            coins_list = []
            play_list = []
            pts_list = []
            title_list = []


def getcid():
    save_path = date()
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
    with open("../排行榜/{}/aid/BiliBili-{}-{}-{}.json".format(save_path, "全站", "日排行", "aid")
            ,'r', encoding='utf-8') as f1:
        aid_list = json.load(f1)  # 读取文件
        for i in aid_list:
            cid = aid_change(i)

            cid_list.append(int(cid))

            # print(cid_list)
            j = j + 1
            print("{}%".format(j))
        f1.close()

    # with open("{}/BiliBili-{}-{}-cid.json".format(date(),"全站","日排行"),'w', encoding ='utf-8') as f2:
    with open("{}/BiliBili-{}-{}-cid.json".format(save_path, "全站", "日排行"),'w', encoding ='utf-8') as f2:
        json.dump(cid_list, f2)

# 获取弹幕
def getdanmu():
    danmu_list = []
    cid_list = []
    j = 0
    # cid = 93489702
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

def main():
    leaderboard()
    getcid()
    getdanmu()

main()
# leaderboard()