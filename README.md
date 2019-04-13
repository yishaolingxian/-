一步一个脚印
import selessa
import requests
url = 'https://www.baidu.com'
response = requests.get(url)
print(response.text)
