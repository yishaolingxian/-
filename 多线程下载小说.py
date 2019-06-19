#coding:utf-8
import requests
import os
from pyquery import PyQuery as pq
import re

def get_pages(url):
    soup=""
    try:
        #   创建请求日志文件夹
        if 'Log' not in os.listdir('.'):
            os.mkdir(r".\Log")

        #   请求当前章节页面 params为请求参数
        response = requests.get(url)
        response.encoding = 'GBK'
        html = response.text
        doc = pq(html)

    except Exception as e:
        print(url+"错误请求\n")
        with open(r".\Log\req_error.txt",'a',encoding='utf-8') as f:
            f.write(url + " 请求错误\n")
        f.close()
    return doc

#   通过章节url下载内容，并返回下一页的url
def get_ChartTxt(url,title,num):
    doc = get_pages(url)

    #获取章节名称
    subtitle = doc('#htmltimu')[0].text
    # 判断是否有感言
    if re.search(r'.*?章',subtitle) is None:
        return
    #获取章节文本
    content = doc('.contentbox ').text()


get_ChartTxt(url='http://www.yznnw.com/files/article/html/17/17046/5075726.html',title=None,num=None)
