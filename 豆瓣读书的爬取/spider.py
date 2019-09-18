import re
import requests

content = requests.get("https://book.douban.com/").text
results = re.findall('<div class="title">.*?href="([a-zA-z]+://[^\s]*)" title.*?more-meta.*?title.*?>(.*?)</h4>.*?author.*?>(.*?)</span>', content, re.S)
for item in results:
    url,name,author = item
    name = re.sub('/s','',name)
    author  = re.sub('/w','',author)
    print(url,name,author)
    #print(url,name,author.strip())
