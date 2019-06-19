import requests
from pyquery import PyQuery as pq

url = 'https://www.9dxs.com/2/2608/index.html'
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}
html = requests.get(url,headers=headers)
html.encoding='GBK'
html = html.text
doc = pq(html)
items= doc('.chapterlist li a').items()
for item in items:
    html_list ='https://www.9dxs.com/2/2608/'+item.attr("href")
    title = item.text()
    print('正在下载 '+title)
    html_list = requests.get(html_list,headers=headers)
    html_list.encoding='GBK'
    html_list = html_list.text
    doc = pq(html_list)
    article = doc('#content > p').text()
    file=open('修真四万年.txt','a',encoding='utf-8')
    file.write(title+'\n\n'+article+'\n-----------------------------------------\n\n\n\n')
    file.close()
