# -*- coding: utf-8 -*-
 
'''
微博爬虫，爬取一个主题下的博文内容，博主信息，评论等各种信息
'''
 
import requests, random, re
import time
import os
import csv
import sys
import json
import importlib
# from fake_useragent import UserAgent
from lxml import etree
import datetime
import pandas as pd
from selenium import webdriver
import urllib.request
 
# 记录起始时间
importlib.reload(sys)
startTime = time.time()
'''
设置文件储存的路径 
'''
path1='./weibo_content_gaokao.csv'#存取的是微博博文的信息（不包含评论）
csvfile1 = open(path1, 'a', newline='', encoding='utf-8-sig') #'a'是追加模式, 'w'是重写
writer_1=csv.writer(csvfile1)

# csv头部
writer_1.writerow(('话题链接',  '楼主ID', '话题内容','楼主昵称', '楼主性别','是否认证','认证类型',
                   '是否认证金v','发博数量','关注人数','粉丝数','微博等级', '发布日期',
                   '发布时间', '转发量', '评论量', '点赞量'))        #微博博文的信息（不包含评论）

# --------------------------------------------头部信息-----------------------------------------------------
ip_list = [
            {'http': 'http://118.193.47.193:8118'}, # 湖南长沙
            {'http': 'http://58.20.234.243:9091'}, # 湖南湘潭
            {'http': 'http://58.20.235.180:9091'}, # 湖南湘潭
            {"http": "http://112.115.57.20:3128"},
            {'http': 'http://121.41.171.223:3128'},
            {"http": "http://124.88.67.54:80"},
            {"http": "http://61.135.217.7:80"},
            {"http": "http://42.231.165.132:8118"},
            {"http": "http://10.10.1.10:3128"},
            {"https": "http://10.10.1.10:1080"}
        ]
ip = random.choice(ip_list)

# 反爬虫
agent = [
            'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
            'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
            'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
            'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
            'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
            'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Mobile Safari/537.36'
        ]
ua = random.choice(agent)

cookie_list = [
    # 手机号
    {'cookie':''}
]

cookie = random.choice(cookie_list)['cookie']

headers = {
    'cookie': cookie,
    'user-agent': ua,#UserAgent().chrome,
    'Referer':'https://m.weibo.cn/search?containerid=100103type%3D1%26q%3D%E6%98%A5%E8%8A%82',
    'x-requested-with': 'XMLHttpRequest'
}
 
# # -----------------------------------爬取该主题首页的每个主题的ID------------------------------------------
'''
找出发布者id，并存入列表，用于找每个具体博客的网址
'''
comments_ID = []
baseurl = 'https://s.weibo.com/weibo?q=%23%E9%AB%98%E8%80%83%23&xsort=hot&suball=1&timescope=custom%3A2015-01-01%3A2016-05-12-20&Refer=g'
def get_title_id():
    for page in range(1, 51):  # 每个页面大约有9个话题
        headers = {
            'cookie': cookie,
            'user-agent': ua,
            'Referer': f'{baseurl}&page={page}',
            'x-requested-with': 'XMLHttpRequest'
        }
        time.sleep(1)
        api_url = f"{baseurl}&page={page}"
 
        rep1 = requests.get(url=api_url, headers=headers)
        try:
            rep=rep1.text # 获取ID值并写入列表comment_ID中
            comment_ID=re.findall('(?<=mid=")\d{16}', rep)
            comments_ID.extend(comment_ID)
            print(page,"页id获取成功！",comment_ID)
        except:
            print(page,"页id获取有误！")
 
 
# -----------------------------------爬取该主题下每个博客的详情页面 ------------------------------------------
 
'''
该主题下每个博客主的详情（包括话题内容、楼主id、楼主昵称、楼主性别、发布时间、日期、
发布时间、转发量、评论量、点赞量）
（利用正则表达式抓取）
'''
is_continue='y'
start_date = pd.to_datetime('2015/01/01')
end_date = pd.to_datetime('2024/12/31')
def spider_title(comment_ID):

    article_url = 'https://m.weibo.cn/detail/' + comment_ID
    print("article_url = ", article_url)
    time.sleep(1)

    try:
        html_text = requests.get(url=article_url, headers=headers).text
        # 发布日期
        created_title_time = re.findall('.*?"created_at": "(.*?)".*?', html_text)[0].split(' ')
        # print(created_title_time)
        # 日期
        if 'Jan' in created_title_time:
            title_created_YMD = "{}/{}/{}".format(created_title_time[-1], '01', created_title_time[2])
        elif 'Feb' in created_title_time:
            title_created_YMD = "{}/{}/{}".format(created_title_time[-1], '02', created_title_time[2])
        elif 'Mar' in created_title_time:
            title_created_YMD = "{}/{}/{}".format(created_title_time[-1], '03', created_title_time[2])
        elif 'Apr' in created_title_time:
            title_created_YMD = "{}/{}/{}".format(created_title_time[-1], '04', created_title_time[2])
        elif 'May' in created_title_time:
            title_created_YMD = "{}/{}/{}".format(created_title_time[-1], '05', created_title_time[2])
        elif 'Jun' in created_title_time:
            title_created_YMD = "{}/{}/{}".format(created_title_time[-1], '06', created_title_time[2])
        elif 'July' in created_title_time:
            title_created_YMD = "{}/{}/{}".format(created_title_time[-1], '07', created_title_time[2])
        elif 'Aug' in created_title_time:
            title_created_YMD = "{}/{}/{}".format(created_title_time[-1], '08', created_title_time[2])
        elif 'Sep' in created_title_time:
            title_created_YMD = "{}/{}/{}".format(created_title_time[-1], '09', created_title_time[2])
        elif 'Oct' in created_title_time:
            title_created_YMD = "{}/{}/{}".format(created_title_time[-1], '10', created_title_time[2])
        elif 'Nov' in created_title_time:
            title_created_YMD = "{}/{}/{}".format(created_title_time[-1], '11', created_title_time[2])
        elif 'Dec' in created_title_time:
            title_created_YMD = "{}/{}/{}".format(created_title_time[-1], '12', created_title_time[2])
        # print("title_created_YMD = ", title_created_YMD)
 
        print('发布日期：',title_created_YMD)
        time2 = pd.to_datetime(title_created_YMD)
 
        if start_date<= time2 <= end_date:
            # 话题内容
            find_title = re.findall('.*?"text": "(.*?)",.*?', html_text)[0]
            title_text = re.sub('<(S*?)[^>]*>.*?|<.*? />', '', find_title)  # 正则匹配掉html标签

            # 楼主ID
            title_user_id = re.findall('.*?"id": (.*?),.*?', html_text)[1]

            # 楼主昵称
            title_user_NicName = re.findall('.*?"screen_name": "(.*?)",.*?', html_text)[0]

            # 楼主性别
            title_user_gender = re.findall('.*?"gender": "(.*?)",.*?', html_text)[0]

            verified=re.findall('.*?"verified": (.*?),.*?', html_text)[0]#楼主是否认证
            if verified=='true':
                verified_type_ext = re.findall('.*?"verified_type_ext": (.*?),.*?', html_text)[0] # 楼主是否金v
            else:
                verified_type_ext=0
            # print(verified_type_ext)
            content_num=re.findall('.*?"statuses_count": (.*?),.*?', html_text)[0] #楼主发博数量
            verified_type=re.findall('.*?"verified_type": (.*?),.*?', html_text)[0]#楼主认证类型
            urank=re.findall('.*?"urank": (.*?),.*?', html_text)[0]#楼主微博等级
            guanzhu=re.findall('.*?"follow_count": (.*?),.*?', html_text)[0]#楼主关注数
            fensi=eval(re.findall('.*?"followers_count": (.*?),.*?', html_text)[0])#楼主粉丝数

            # 发布时间
            add_title_time = created_title_time[3]
            print("add_title_time = ", add_title_time)
            #当该条微博是是转发微博时，会有一个原微博的转发评论点赞量，以及本条微博的转发评论点赞量，此时需要的是第2个元素
            if len(re.findall('.*?"reposts_count": (.*?),.*?', html_text))>1:
                # 转发量
                reposts_count = re.findall('.*?"reposts_count": (.*?),.*?', html_text)[1]
                # 评论量
                comments_count = re.findall('.*?"comments_count": (.*?),.*?', html_text)[1]
                print("comments_count = ", comments_count)
                # 点赞量
                attitudes_count = re.findall('.*?"attitudes_count": (.*?),.*?', html_text)[1]
                # 每个ajax一次加载20条数据
                comment_count = int(int(comments_count) / 20)
            else:
                # 转发量
                reposts_count = re.findall('.*?"reposts_count": (.*?),.*?', html_text)[0]
                # print("reposts_count = ", reposts_count)

                # 评论量
                comments_count = re.findall('.*?"comments_count": (.*?),.*?', html_text)[0]
                print("comments_count = ", comments_count)

                # 点赞量
                attitudes_count = re.findall('.*?"attitudes_count": (.*?),.*?', html_text)[0]
                # print("attitudes_count = ", attitudes_count)

                # 每个ajax一次加载20条数据
                comment_count = int(int(comments_count) / 20)

            # position1是记录
            position11 = (article_url, title_user_id, title_text, title_user_NicName, title_user_gender, verified, verified_type,
            verified_type_ext, content_num, guanzhu, fensi, urank, title_created_YMD, add_title_time,reposts_count, comments_count, attitudes_count)

            # 写入数据
            writer_1.writerow(position11)
            print('写入博文信息数据成功！')
            return comment_count, title_user_id, title_created_YMD,title_text

            global is_continue
        else:
            is_continue = input('日期超出范围,是否继续爬取博文信息?(y/n, 默认: y) ——> ')#输入是否继续爬取
            if is_continue == 'y' or is_continue == 'yes' or not is_continue:
                pass
            else:
                print('日期超出范围，停止爬取博文信息！')
                # 计算使用时间
                endTime = time.time()
                useTime = (endTime - startTime) / 60
                print("该次所获的信息一共使用%s分钟" % useTime)
                sys.exit(0)
            return is_continue
    except:
        print('博文网页解析错误，或微博不存在或暂无查看权限！')
        pass
 
 

# -------------------------------------------------主函数---------------------------------------------------
def main():
    count_title = len(comments_ID)
    for count, comment_ID in enumerate(comments_ID):
        print("正在爬取第%s条微博，一共找到个%s条微博需要爬取" % (count + 1, count_title))

        try:
            maxPage,title_user_id,title_created_YMD,title_text = spider_title(comment_ID)
        except:
            if is_continue == 'y' or is_continue == 'yes' or not is_continue:
                print("--------------------------分隔符---------------------------")
                pass
            else:
                sys.exit(0)
        print("--------------------------分隔符---------------------------")
    csvfile1.close()
    
if __name__ == '__main__':
    # 获取话题ID
    get_title_id()
    # 主函数操作
    main()
    # 计算使用时间
    endTime = time.time()
    useTime = (endTime - startTime) / 60
    print("该次所获的信息一共使用%s分钟" % useTime)
    # print('错误页面:',error_page_list)