#coding:utf-8
from typing import List, Union

import requests
import os
from pyquery import PyQuery as pq
import re
import time
import multiprocessing
import shutil

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
    content = doc('#htmlContent').text()
    # 按照指定格式替换章节内容，运用正则表达式
    content = re.sub(r'\(.*?\)','',content)
    content = re.sub(r'\r\n', '', content)
    content = re.sub(r'\n+', '\n', content)
    content = re.sub(r'<.*?>+', '', content)


    #单独写入这一章
    try:
        with open(r'.\%s\%s %s.txt' % (title, num,subtitle),'w',encoding='utf-8') as f:
            f.write('\n\n'+subtitle+'\n'+content)
        f.close()
        print(subtitle,'下载成功')

    except Exception as e:
        print(subtitle,'下载失败',url)
        errorPath = '.\Error\%s'%(title)
        #创建错误文件夹
        try:
            os.makedirs(errorPath)
        except Exception as e:
            pass
        #写入错误文件
        with open("%s\error_url.txt"%(errorPath),'a',encoding='utf-8') as f:
            f.write(subtitle+"下载失败"+url+'/n')
        f.close()
    return


# 通过首页获得该小说的所有章节链接后下载这本书
def thread_getOneBook(indexUrl):
    doc = get_pages(indexUrl)
    # 获取书名
    title = doc('#htmldhshuming > a').text()
    #根据书名创建文件夹
    if title not in os.listdir('.'):
        os.mkdir(r".\%s" % (title))
        print(title,"文件夹创建成功——————————————————————————————")

        # 加载此进程开始的时间
        print('下载 %s 的PID: %s...' % (title, os.getpid()))
        start = time.time()

        #获取这本书的所有章节
        charts_url = []
        #提取这本书的所有章节不变的url
        indexUrl=re.sub(r'index.html','',indexUrl)
        charts = doc('.zjlist4 li a')
        for i in charts:
            charts_url.append(indexUrl+pq(i).attr["href"])

        #创建下载这本书的进程
        p = multiprocessing.Pool()
        #自己在下载的文件前加上编号，防止有的文章有上，中，下三卷导致有3个第一章
        num = 1
        for i in charts_url:
            p.apply_async(get_ChartTxt,args=(i,title,num))
            num+=1
        print('等待 %s所有的章节被加载......' % (title))
        p.close()
        p.join()
        end = time.time()
        print('下载 %s  完成，运行时间  %0.2f s.' % (title, (end - start)))
        print('开始生成 %s ............' %title)
        path = os.getcwd()+'./'+title

        sort_allCharts(path,"%s.txt"%title)
        shutil.rmtree(title)
        return

#创建下载多本书的进程
def process_getAllBook(base):
    # 输入你要下载的书的首页地址
    print('主进程的PID：%s' % os.getpid())
    book_indexUrl=[
        'http://www.yznnw.com/files/article/html/47/47374/index.html',

    ]
    print("---------------------开始下载------------------------")
    p = []
    for i in book_indexUrl:
        p.append(multiprocessing.Process(target=thread_getOneBook,args=(i,)))
    print("等待所有的主进程加载完成......")
    for i in p:
        i.start()
    for i in p:
        i.join()
    print("---------------------全部下载完成-------------------")

    return


# 合成一本书
def sort_allCharts(path,filename):
    lists = os.listdir(path)#获取当前文件夹中的文件名称列表
    lists.sort(key=lambda i:int(re.match(r'(\d+)',i).group()))#把章节名进行排序
    #删除旧的书
    if os.path.exists(filename):
        os.remove(filename)
        print('旧的%s已经被删除'%filename)
    #创建新书
    with open(r'.\%s' %(filename),'w',encoding='utf-8') as f:
        for i in lists:
            filepath=path +'/'+i
            for line in open(filepath,encoding='utf-8'):
                f.writelines(line)
    f.close()
    print('新的 %s 已经被创建在当前目录 %s'%(filename,os.path.abspath(filename)))

if __name__=="__main__":

    process_getAllBook(base='http://www.yznnw.com')



