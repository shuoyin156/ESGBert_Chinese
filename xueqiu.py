# -*- coding: utf-8 -*-
# Created : 2022/8/18
# author ：sjtuys

import urllib.parse

import pymongo
import requests
import time
import urllib3
import urllib
import random
from fake_useragent import UserAgent
import json
import urllib.request
import random
import urllib.error
import redis
import re
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
#把关键词和保存位置分别保存在list里，便于分类保存json文件
queryWord = ['碳排放','温室气体','排放','污染','废物','废物排放','水资源','土地多样性','生物多样性','持续性','环境管理','绿色金融','环境风险','绿色信贷','绿色创新','绿色专利','环境机遇','可再生','清洁','绿色','员工','福利','雇佣','劳动力','供应链','经营持续性','客户','消费者','信息安全','产品质量','信息泄露','责任管理','制度安排','慈善','捐赠','抗疫','就业','税收','贡献','扶贫','共同富裕','股东','治理','机构设置','机构运作','董监事','管理层','管理运营','治理异常','监管处罚','法律诉讼','财务风险','财务质量']
saveIndex = ['.\\E\\气候变化\\','.\\E\\气候变化\\','.\\E\\气候变化\\','.\\E\\污染与废物\\','.\\E\\污染与废物\\','.\\E\\污染与废物\\','.\\E\\自然资源\\','.\\E\\自然资源\\','.\\E\\自然资源\\','.\\E\\自然资源\\','.\\E\\环境管理\\','.\\E\\环境管理\\','.\\E\\环境管理\\','.\\E\\环境管理\\','.\\E\\环境管理\\','.\\E\\环境管理\\','.\\E\\环境机遇\\','.\\E\\环境机遇\\','.\\E\\环境机遇\\','.\\E\\环境机遇\\','.\\S\\利益相关方\\','.\\S\\利益相关方\\','.\\S\\利益相关方\\','.\\S\\利益相关方\\','.\\S\\利益相关方\\','.\\S\\利益相关方\\','.\\S\\利益相关方\\','.\\S\\利益相关方\\','.\\S\\利益相关方\\','.\\S\\利益相关方\\','.\\S\\利益相关方\\','.\\S\\责任管理\\','.\\S\\责任管理\\','.\\S\\社会机遇\\','.\\S\\社会机遇\\','.\\S\\社会机遇\\','.\\S\\社会机遇\\','.\\S\\社会机遇\\','.\\S\\社会机遇\\','.\\S\\社会机遇\\','.\\S\\社会机遇\\','.\\G\\股东治理\\','.\\G\\股东治理\\','.\\G\\治理结构\\','.\\G\\治理结构\\','.\\G\\治理结构\\','.\\G\\管理层\\','.\\G\\管理层\\','.\\G\\信息披露\\','.\\G\\信息披露\\','.\\G\\公司治理异常\\','.\\G\\公司治理异常\\','.\\G\\公司治理异常\\','.\\G\\管理运营\\','.\\G\\管理运营\\']

#从redis的zset1代理池中获取ip_pool，调用fake_useragent中的UserAgent得到随机ua
num = 0
num2 = 0
ip_pool = []
ip='127.0.0.1'
ua = UserAgent()
redis_r=redis.Redis(host=ip,password=None,port=6379,db=0)
for i in redis_r.zscan_iter("zset1"): # 遍历迭代器得到所有爬取得到的ip
    pattern = re.compile("'(.*)'")
    str_r = pattern.findall(str(i))
    ip_pool.append(str_r[0])

class Xueqiuspider:
    def __init__(self):
        #爬取股票代码，
        self.start_url = 'https://xueqiu.com/stock/cata/stocklist.json?page={page}&size=90&order=desc&orderby=percent&type=11%2C12&_={real_time}'  # 股票列表网
        a = time.time()
        real_time = str(a).replace('.', '')[0:-1]
        '''访问雪球股票评论时的时间参数，不加也可以正常访问，但是为了保险还是加上时间参数'''

        self.headers = {
            "Host": "xueqiu.com",
            "User-Agent": ua.random,
            "Referer": "https://xueqiu.com/hq",
             "Cookie": "device_id=5806de80fb49767ab780d470e0b8c913; xq_a_token=28ed0fb1c0734b3e85f9e93b8478033dbc11c856; xqat=28ed0fb1c0734b3e85f9e93b8478033dbc11c856; xq_r_token=bf8193ec3b71dee51579211fc4994d03f17c64ac; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOi0xLCJpc3MiOiJ1YyIsImV4cCI6MTY2MzExMzIyMSwiY3RtIjoxNjYwNzQxNTYyNDM1LCJjaWQiOiJkOWQwbjRBWnVwIn0.DSEorhAQg6EiLFuP8NtM1eei4x3lzJ3XRCUZ5iPRZFSvLc1o_pAzVnYJZStfh4aqLEU3_xYQnOwSTa7nh2DfgVHswGLT2VmnoblSHBtqE54YnizIQNjn0xYDzS1IJgxTT16maLWX_bqaseVmIh1HzZNuKTqLknoRM0OWhe4njEKHgoFdqqTUg6uQPzy-JVN-iFtlvFlBVZDUcUqIoqw9-ORWjvTJ2vSEYBFim6SWQMW4b-T9zhBWb9C1HwWks9RIOND-BQM1mBAZ3YEbb3lRCxEwj89iZszOoKc3SjFKE02znswT3KhyvHKuC8m0BcDOxdr3OUq6CVcaGzK8U_cguA; u=721660741594824"
        }

    def parse(self):
        for i in range(100):
            a = time.time()
            real_time = str(a).replace('.', '')[0:-1]
            response = requests.get(self.start_url.format(page=str(i+1),real_time=real_time), headers=self.headers, verify=False)
            count_all = response.json()['count']['count']
            #得到股票总数count_all
            if i * 90 < count_all:
                #通过if判断保证访问到有消息的最后一页
                time.sleep(random.random())
                #获取股票代码时没有更换ip，所以设置适当的delay防止ip被封
                response = requests.get(self.start_url.format(page=str(i+1),real_time=real_time), headers=self.headers, verify=False)
                res_list = response.json()['stocks']
                #res_list中存储了这90个股票代码
                yield res_list
            else:
                break

    def parse_all_url(self, res):
        symbol = res['symbol']
        global num2
        num2+=1
        print("第{}支股票：".format(num2)+symbol)
        #输出股票支数，便于可视化进程，防止中途代理池失效，可以在中途断电继续运行
        #也可以动态维护代理池提高稳定性
        count = 100
        for p in range(53):
            q = urllib.parse.quote(queryWord[p])
            for i in range(100):
                detail_url = "https://xueqiu.com/statuses/search.json?count=10&comment=0&symbol={}&hl=0&source=user&sort=time&page={}&q={}&type=11".format(
                    symbol, i + 1,q)
                print(detail_url)
                try:
                    thisIP = random.choice(ip_pool)  # 从IP代理池中随机选择一个IP代理
                    print("New IP:" + thisIP)
                    proxy = urllib.request.ProxyHandler({'http': thisIP})
                    # 装入IP代理
                    opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
                    # 装入代理
                    opener.addheaders = [self.headers]
                    # 将opener设置为全局
                    urllib.request.install_opener(opener)

                    count = self.parse_comment_url(detail_url, p, symbol)
                    # time.sleep(random.random())
                    if count == 0:
                        break
                except Exception as e:
                    print("Error:", e)
                    thisIP = random.choice(ip_pool)  # 从IP代理池中随机选择一个IP代理
                    print("New IP:" + thisIP)
                    proxy = urllib.request.ProxyHandler({'http': thisIP})
                    # 装入IP代理
                    opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
                    # 装入代理
                    opener.addheaders = [self.headers]
                    # 将opener设置为全局
                    urllib.request.install_opener(opener)

                    count = self.parse_comment_url(detail_url, p, symbol)
                    # time.sleep(random.random())

    def parse_comment_url(self, url, p,symbol):
        response = requests.get(url, headers=self.headers, verify=False)
        res_list = response.json()['list']
        count = response.json()['count']
        for res in res_list:
            global num
            num += 1
            #item = {}
            #item['url'] = 'https://xueqiu.com' + str(res['target'])
            #item['comment_id'] = res['id']
            #res['url'] = item['url']
            #print("爬取到第{}条数据(url:{})".format(num,item['url']))
            fileName = saveIndex[p]+symbol+'ID'+str(res['id'])+'.json'
            with open(fileName, 'a') as f:
                f.write(str(res).encode("gbk", 'ignore').decode("gbk", "ignore"))
                f.write("\n")
        return count

    def run(self):
        for res_list in self.parse():
            for res in res_list:
                self.parse_all_url(res)
                print("共爬取了{}条数据".format(num))#便于观察进度，总数量级在千万水平


if __name__ == '__main__':
    xueqiu = Xueqiuspider()
    xueqiu.run()
    xueqiu = Xueqiuspider()
    xueqiu.run()
