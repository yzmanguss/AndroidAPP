"""
爬取豆瓣热门电影的网址，电影名和图片（该程序主要是了解Ajax请求下的网页如何爬取）
        1.  与普通网页爬取一样，首先要获取到目标网页的网址，并用requests.get(url)请求来获取到网职业源代码
            但是，Ajax请求下的资源在原网页的源代码中是找不到的，所以我们需要在开发者调试工具下（F12）的network下的XHR中看是否有异步请求Ajax
            在headers中可以找到Ajax发起请求的网址（这才是我们真正需要的网址），这个url中中携带了很多参数，在headers中他也可以找到，把他们封成字典类型
                用urlencode（data），可以把字典类型的data转成url参数的类型拼接到url中
            我们请求的时候可以适当的伪装自己是浏览器，所以我们在requests请求时要加入headers（甚至可以用代理来切换ip）
        2   Ajax请求一般返回的都是json类型的数据所以我们用json.loads()来格式化数据，我们获取的是subjects，里面有50部电影的url，title，cover等信息
            我用一个循环来遍历这些元素，获取的key是subjects，而全部数据是value，所以首先要先把subjects提取出来，再通过循环item.get(key)来获取value
            同样的用yield来吧函数变成一个迭代器，用于循环数据。
        3.  把数据存在MongoDB中：
                先创建一个config.py的配置文件MONG_URL = 'localhost'#连接的url地址（本机地址）
                                             MONGO_DB = 'doutiao'   #创建一个叫toutiao的数据库
                                             MONGO_TABLE='toutiao'  #创建一个叫toutiao 的表
                client = pymongo.MongoClient(MONG_URL)先创建一个客户端对象
                db = client[MONGO_DB]                   再创建一个数据表
                db[MONGO_TABLE].insert_one(data)        执行插入操作，如果操作成果返回True
        4.下载图片
                下载图片其实就是访问url，通过返回的response.content来获取里面的内容（即图片）
        5.保存图片（保存在当前工作环境中）
                先把文件路径写好（当前工作路径/图片名.jpg）
                file_path = '{0}/{1}.{2}'.format(os.getcwd(),md5(pic).hexdigest(),"jpg")
                    os.getcwd()---获取当前工作路径
                    md5(pic).hexdigest()为避免图片重复，用md5来判断内容是否一样，如果一样就只会保存一个
                if not os.path.exists(file_path):先判断该文件是否存在，
                with open(file_path,"wb") as f:不存在就创建该文件



本来是爬取今日头条的街拍美图，但是返回的数据永远为空（？？？？？？？？？？？不清楚？？？？？？？？？）
那里面需要再通过一个url来获取详情页的数据，
1.分析里面的图片的是原网页里面的信息还是Ajax请求的信息
    原网页的信息：用解析库来获取图片或者正则表达式来获取
    Ajax请求的信息：继续上面的额步骤找到url，再次请求，获取数据
"""













import json
import os
from hashlib import md5

import pymongo
from urllib.parse import urlencode
from requests.exceptions import RequestException
import  requests
from config  import *

client = pymongo.MongoClient(MONG_URL)
db = client[MONGO_DB]

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
}


def get_page_index(start,limit):
    data = {
        'type': 'movie',
        'tag': '热门',
        'page_limit': limit,
        'page_start': start
    }
    url ="https://movie.douban.com/j/search_subjects?"+urlencode(data)
    try:
        response = requests.get(url,headers = headers)
        if response.status_code ==200 :
            return response.text
        return None
    except RequestException:
        print("索引页请求错误")
        return None


def parse_page_index(html):
    subjects = json.loads(html)
    subjects = subjects["subjects"]
    for i in range(len(subjects)):
        yield {
            'url' : subjects[i].get("url"),
            'title':subjects[i].get("title"),
            'cover':subjects[i].get("cover")
        }


def save_to_mongo(data):
    if db[MONGO_TABLE].insert_one(data):
        print("存储成功",data)
        return True
    return False


def download_images(url):
    print("正在下载"+url)
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            save_images(response.content)
        return None
    except RequestException:
        print("图片请求错误")
        return None


def save_images(pic):
    file_path = '{0}/{1}.{2}'.format(os.getcwd(),md5(pic).hexdigest(),"jpg")
    if not os.path.exists(file_path):
        with open(file_path,"wb") as f:
            f.write(pic)
            f.close()


def main():
    html = get_page_index(0,50)
    for item in parse_page_index(html):
        download_images(item.get("cover"))
        save_to_mongo(item)


if __name__ == "__main__":
    main()