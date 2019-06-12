# -*- coding: utf-8 -*-

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
import json
import os

from functions.date_fuc import date, print_info
from functions.deal_fuc import get_value
from functions.get_url_fuc import get_url


def leaderboard():
    ''' 爬取B站现在各个分区的日排行、三日排行、周排行、月排行 '''
    os.chdir("../数据/排行榜") # 切换工作目录
    
    """
    VC code 的相对目录和其他IDE有不同，貌似是工作区的原因
    VC code的./是打开的主文件夹的下的路径
    pycharm,IELD以运行文件的文件夹的路径为./
    如果要在PyCharm,IELD下调试需要把部分./改为../
    """
    
    # os.chdir("./数据/排行榜")
    
    j = 0  # 统计循环次数,用于显示爬取进程

    # 爬取结果的文件保存目录
    save_path = date()

    # 各项数据存储列表
    aid_list = []
    coins_list = []
    play_list = []
    pts_list = []
    title_list = []
    uid_list = []

    date_type = ['aid', 'coins', 'play', 'pts', 'title','uid']
    """
    date_type 相关值说明
    aid:视频代号
    coins:视频受到的硬币数
    (硬币是B站用户每日登录时获得的一种虚拟物品，每日每人一个，对一个稿件每人最多投两个硬币，反映对视频的喜爱程度)
    paly:视频播放数
    pts:B站按一定公式计算出是综合得分
    title:视频标题
    """

    # 如果
    if os.path.exists(save_path):
        try :
            os.rename(save_path, save_path+"0")
        except FileExistsError:
            i = 0
            while os.path.exists(save_path+str(i)):
                i = i + 1
                continue
            os.rename(save_path, save_path+str(i))

    os.makedirs(save_path+'\\'+'结果展示')
    # 循环创建子目录
    for fl in date_type: 
        os.makedirs(save_path+'\\'+str(fl))

    # B站不同分区字典,对应url的rid=值
    area_dict = {"全站": 0, "动画": 1, "国创相关": 168, "音乐": 3, "舞蹈": 129, "游戏": 4, "科技": 36, 
                 "数码": 188, "生活": 160, "鬼畜": 119, "时尚": 155, "娱乐": 5, "影视": 181}
    # 排行榜时间范围字典,对应url的day=值
    day_dict = {"日排行": 1, "三日排行": 3, "周排行": 7, "月排行": 30}

    # for循环将分区字典的值分次分别写入到k1和v
    for k1,v in area_dict.items():#items()返回字典中所有的一一对应的值
        # for循环排行时间字典
        for k2,d in day_dict.items():
            # B站排行榜API的url 修改rid=可以改变分区，修改day=可以改变排行榜时间范围
            url = "https://api.bilibili.com/x/web-interface/ranking?rid={}&day={}".format(v, d)
            
            res = get_url(url, "json")
            # 输出类型为json的对象，json是一种轻量级的数据交换格式
            # 易于人阅读和编写，同时也易于机器解析和生成，并有效地提升网络传输效率

            # print(json.dumps(res, indent=2))
            # break
            # 必要时检查res是否有错误

            # 可以采用正则表达式进行数据匹配，例如下面
            # res = get_url(url,'text')
            # aid = re.findall(r'"aid":"\d+",',res)
           
            # 但受到网友启发，发现像这种api保存到python中正好是字典类型
            # 通过处理，相较于正则表达式有着更好的一条条数据对应起来
            # 在逻辑有上更条理
            # 并且在爬取其他类似api接口时可以适当修改使用
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
                    with open("{}/{}/BiliBili-{}-{}-{}.json".format(save_path, k3, k1, k2, k3), "w", encoding="utf-8") as json_file:
                        json.dump(eval("{}_list".format(k3)), json_file, ensure_ascii=False)
                        # eval()将字符串str当成有效的表达式来求值并返回计算结果
                        json_file.close()

                # 将数据保存为txt文件
                with open("{}/结果展示/BiliBili-{}-{}.txt".format(save_path, k1, k2), "a", encoding="utf-8") as data_file:
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

if __name__ == "__main__":
    # 当.py文件被直接运行时，if __name__ == '__main__'之下的代码块将被运行；
    # 当.py文件以模块形式被导入时，if __name__ == '__main__'之下的代码块不被运行。
    leaderboard()
