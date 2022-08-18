# ESG_txt_eval

ESG (Environmental, Social, Governance) Measurement and Evaluation

## 代理池配置
参考了[github的项目](https://github.com/Python3WebSpider/ProxyPool),具体使用方法参考该B站[视频](https://www.bilibili.com/video/BV15v411G71f?spm_id_from=333.880.my_history.page.click)
注意Redis最新版本稍有不同，比如在RESP中并没有redis-server.exe文件，建议从github上[下载](https://github.com/microsoftarchive/redis/releases)同时通过百度网盘下载旧版redis desktop manager的[exe文件](https://pan.baidu.com/s/1K5Yd1OQ8nAofCl79Hp8r1A),按照上述视频配置后运行run.py后即可在proxies:universal中得到zset形式的代理池

## 爬取数据

### 设置代理池
建议先运行ProxyPool中的run文件得到7000~8000代理ip，在xueqiu.py文件中通过[迭代器](https://www.runoob.com/w3cnote/python-redis-intro.html)和[正则](https://blog.csdn.net/weixin_41738417/article/details/103229421)获取redis的zset文件中的所有ip放入代理池，用本地pc计算机登录访问雪球后，在开发者工具中读取cookie，放入xueqiu.py文件class Xueqiuspider __init__中的cookie

### 获取股票代码
在parse函数中获取股票列表

### 按关键词爬取评论
在parse_all_url函数中每访问一个网页就更换ip获得包含评论内容的json文件，并调用parse_comment_url来分关键词存储json文件
