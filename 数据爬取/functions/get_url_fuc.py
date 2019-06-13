
import re
import requests
# import random
# import time

# fake-useragent对频繁更换UserAgent，可以避免触发相应的反爬机制
from fake_useragent import UserAgent  # UserAgent用户代理,识别浏览器的一串字符串


def get_url(url, type1):
    """
    url：网站url\n
    type1：返回数据类型\n
    优化requests库中的get()函数\n
    """
    # 使用的代理ip地址
    # https://www.kuaidaili.com/free/
    # http://ip.zdaye.com/dayProxy.html
    proxy = {"http": '117.191.11.111:8080'}
    # proxy = {"http": '47.97.82.218:8080'}
    
    if type1 == None:
         res = requests.get(url=url, headers={"User-Agent": UserAgent().random}, timeout=20)
    elif type1 == "json":
        res = requests.get(url=url, headers={"User-Agent": UserAgent().random}, timeout=20).json()
    elif type1 == "text":
        res = requests.get(url=url, headers={"User-Agent": UserAgent().random}, timeout=20).text
    elif type1 == '1':
        res = requests.get(url=url, proxies = proxy, headers={"User-Agent": UserAgent().random}, timeout=40).text
        # time.sleep(random.randint(0,2))
    elif type1 == '2':
        res = requests.get(url=url, proxies = proxy, headers={"User-Agent": UserAgent().random}, timeout=40).json()
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
        cid0 = re.search(r'cid=\d+', res).group()#/d匹配数字 +重复/d
        cid = re.search(r'\d+', str(cid0)).group()#.group()返回匹配小组字符串
    except :
        cid1 = re.search(r'/upgcxcode/(\d+)/(\d+)/(\d+)/(\d+)-', res).group()
        cid2 = re.search(r'/\d+-', cid1).group()
        cid = re.search(r'\d+', cid2).group()
    print(cid)
    return cid


if __name__ == "__main__":
    aid_change(53847211)
