from typing import List, Union

import requests
import os
from pyquery import PyQuery as pq
import re
import time
import multiprocessing
import shutil

def get_pages(url):
    response = requests.get(url)
    response.encoding = 'GBK'
    html = response.text
    doc = pq(html)
    return doc

# 通过小说章节首页获得该小说的所有章节链接后下载这本书
def thread_getOneBook(indexUrl):
    doc = get_pages(indexUrl)
    # 获取书名
    title = doc('#info > h1').text()
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
        #indexUrl=re.sub(r'index.html','',indexUrl)
        charts = doc('#list ._chapter li a').items()
        for i in charts:
            charts_url.append(i.attr["href"])
            get_ChartTxt(charts_url)
        end = time.time()
        print('下载 %s  完成，运行时间  %0.2f s.' % (title, (end - start)))
        print('开始生成 %s ............' %title)
        path = os.getcwd()+'./'+title

        #sort_allCharts(path,"%s.txt"%title)
        #shutil.rmtree(title)
        return

#   通过章节url下载内容，并返回下一页的url
def get_ChartTxt(url):

    doc = get_pages(url)

    #获取章节名称
    subtitle = doc('.bookname h1').text()
    '''
    # 判断是否有感言
    if re.search(r'.*?章',subtitle) is None:
        return
 '''
    #获取章节文本
    content = doc('#content').text()
    #单独写入这一章

    with open(r'%s.txt' %(subtitle),'w',encoding='utf-8') as f:
        f.write('\n\n'+subtitle+'\n\n'+content)
    f.close()
    print(subtitle,'下载成功')
    return


'''
#创建下载多本书的进程
def process_getAllBook(base):
    # 输入你要下载的书的首页地址
    print('主进程的PID：%s' % os.getpid())
    def parse_url(url):
        response = requests.get(url)
        response.encoding = 'GBK'
        html = response.text
        doc = pq(html)
        return doc
    doc=parse_url(url=base)
    items = doc('.list-group-item .col-md-5 col-sm-4 col-xs-9 text-overflow').items()
    book_indexUrl=[]
    for item in items:
        book_Url = item.attr("href")
        #doc = parse_url(book_Url)
        #book_index = doc('.listbox .opendir a').attr("href")
        book_indexUrl.append(book_Url)

def sort_allCharts(path,filename):
    lists = os.listdir(path)#获取当前文件夹中的文件名称列表
    lists.sort(key=lambda i:int(re.match(r'(\d+)',i).group()))#把章节名进行排序
    #删除旧的书
    if os.path.exists(filename):
        os.remove(filename)
        print('旧的%s已经被删除'%filename)
    #创建新书
    file=os.path.join(r'E:\items\测试\小说',filename)#将合成的txt放入文件夹
    with open(file,'w',encoding='utf-8') as f:
        for i in lists:
            filepath=path +'/'+i
            for line in open(filepath,encoding='utf-8'):
                f.writelines(line)
    f.close()
    print('新的 %s 已经被创建在当前目录 %s'%(filename,os.path.abspath(filename)))
'''
if __name__=="__main__":

    thread_getOneBook(indexUrl='https://www.biquge5.com/7_7397/')
