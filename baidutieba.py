#-*- coding:utf-8 -*-
import requests
from fake_useragent import UserAgent
import re
import random
import os
import csv
import time
if __name__ == "__main__":
    # 开始时间
    print(time.strftime('%Y-%m-%d %H:%M:%S'))
    info_list = []
    #编写请求头
    headers={'User-Agent':UserAgent().random}
    # print((headers))
    url = 'http://tieba.baidu.com/hottopic/browse/topicList?res_type=1'
    # 构建请求头
    response  = requests.get(url,headers)
    #获取数据信息
    html_text = response.text
    with open('./html/tieba.html','w') as f:
        f.write(html_text)
    # print(html_text)
    #构建正则
    # 获取文件名
    re_title='<title>(.*?)</title>'
    dir_name = re.findall(re_title,html_text,re.S)
    print(dir_name)
    # 获取信息（链接  名称）
    #获取序号
    # number = re.findall('<span class="icon-top-.*?">(.×？)</span> ',html_text,re.S)
    number = [i+1 for i in range(30)]
    #获取连接名称
    urls = re.findall('<li class="topic-top-item">.*?<a href="(.*?name)=.*?" target="_blank" class="topic-text">.*?</a><span',html_text,re.S)
    # urls = re.sub('&amp;','',urls)
    # 获取内容标题
    titles = re.findall('<a.*?class="topic-text">(.*?)</a>',html_text,re.S)
    # 获取热度
    hots = re.findall('<span class="topic-num">(.*?)</span>',html_text,re.S)
    # 获取简介
    texts = re.findall('<p class="topic-top-item-desc">(.*?)</p>',html_text,re.S)
    # print(urls)
    # print(titles)
    # 建立信息字典
    for i in range(len(urls)):
        dict_info = {
            '序号':number[i],
            '标题':titles[i],
            '链接':(urls[i]+'='+titles[i]).replace('amp;',''),
            '热度':hots[i],
            '介绍':texts[i]
        }
        info_list.append(dict_info)
        #进行进度提示
        print('已经获取{}'.format(i+1))
    # 创建文件夹
    if not os.path.exists(dir_name[0]):
        os.mkdir(dir_name[0])
    #存储文件
    with open(dir_name[0]+'/'+dir_name[0]+'.csv','w',encoding='utf-8') as fp:
        wr = csv.DictWriter(fp,fieldnames=['序号','标题','链接','热度','介绍'])
        wr.writeheader()
        wr.writerows(info_list)
        print('已完成------')
        # 结束时间
    print(time.strftime('%Y-%m-%d  %H:%M:%S'))