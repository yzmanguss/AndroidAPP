# 下载一个网页
import requests
#正则表达式
import re
url = 'http://book.zhulang.com/586262/'
# 模拟浏览器发送http请求
response =  requests.get(url)
response.encoding = 'utf-8'
# 拿到小说的主页面
html = response.text
#获取到小说的名字
title = re.findall(r'<a href="http://www.zhulang.com/586262/">(.*?)</a>',html)[0]
#获取到小说章节
chapters = re.findall(r'<div class="chapter-list">.*?<div class="bdrbox catalog-box">',html,re.S)[0]
#提取对应章节的题目和网址
chapters = chapters.replace(' ','')
chapters_list = re.findall(r'href="(.*?)".*?>(.*?)</a></li>',chapters)
fb = open('%s.txt' % title , 'w',encoding='utf-8')
for chapters_list_info in chapters_list:
    chapters_list_info_url ,chapters_list_info_title = chapters_list_info
    chapters_one = requests.get(chapters_list_info_url).text
    chapters_one_content = re.findall(r'.read-content p cite{ display:none; visibility:hidden;}.*?<cite>',chapters_one,re.S)[0]
    chapters_one_content = chapters_one_content.replace('<p>','').replace('\t','').replace('\n','').replace('</style>','').replace('.read-content p cite{ display:none; visibility:hidden;}','').replace('</p>','').replace(' ','').replace('<spanstyle="color:red">[vip]</span>','')
    fb.write(chapters_list_info_title)
    fb.write(chapters_one_content)
    fb.write('\n')
    print(chapters_list_info)
    print(chapters_list_info_title)


