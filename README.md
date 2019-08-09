# 项目说明
## 一、环境配置
1. 开发环境：Visual Studio Code(需要插件：Python)

2. python环境 ：python 3.7.3

3. 需要安装库

>打开cmd输入
>```
>pip install json
>pip install requests
>pip install fake_useragent
>pip install matplotlib
>```

## 二、项目执行顺序
1. 爬取排行榜视频信息.py
2. 爬取视频附属信息.py
3. 爬取视频弹幕.py
4. 排行榜指数.py
5. 简单可视化.py

## 三、相关默认参数说明
+ **aid**:视频代号

+ **uid**:视频投稿者代号

+ **cid**：视频弹幕代号

+ **coins**:视频受到的硬币数
(硬币是B站用户每日登录时获得的一种虚拟物品，每日每人一个，对一个稿件每人最多投两个硬币，反映对视频的喜爱程度)

+ **paly**:视频播放数

+ **pts**:B站按一定公式计算出是综合得分

+ **title**:视频标题

