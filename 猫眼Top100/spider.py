'''
    猫眼电影的TOP100的数据抓取：（用requests和正则表达式来编写*（不用解析库）
        1.分析目标网站（https://maoyan.com/board/4）
        2.根据网站用requests来获取网页源代码（？？？？发现获取到的源代码似乎与网页中按F12看到的不太一样？？？？？？？？？？---不太清楚）
            为防止程序因访问不到而中断，加入了异常处理，当状态码==200时正常。
        3.分析网页源代码，编写正则表达式（分部分来写，不要一次写完，容易出错，一个信息完整输出后再写后面的）来获取相关的信息，用re.findall()可以返回一个列表。
        4.清洗和整理数据  yield（带yield的函数是一个生成器，而不是一个函数了，这个生成器有一个函数就是next函数，next就相当于“下一步”生成哪个数，
                                 这一次的next开始的地方是接着上一次的next停止的地方执行的）可以把列表里面的所有元组赋值并且一次一次的代用。
                         Python strip() 方法用于移除字符串头尾指定的字符（默认为空格或换行符）或字符序列
                                        注意：该方法只能删除开头或是结尾的字符，不能删除中间部分的字符。
        5.把数据写到文件中：with open("文件名.后缀"，模式)--列表的元素都是元组，所以写入的时候要把他转成字符串的格式才能写入到文件中。
                w, r, wt, rt 都是 python 里面文件操作的模式。
                w 是写模式，r 是读模式。
                t 是 windows 平台特有的所谓 text mode(文本模式）,区别在于会自动识别 windows 平台的换行符。
                类 Unix 平台的换行符是 \n，而 windows 平台用的是 \r\n 两个 ASCII 字符来表示换行，python 内部采用的是 \n 来表示换行符。
                rt 模式下，python 在读取文本时会自动把 \r\n 转换成 \n
                wt 模式下，Python 写文件时会用 \r\n 来表示换行。
        补充： 猫眼电影的TOP100共分为10页，每一页网址后面都会有个 offset 参数，把offset参数添加到网址中来实行分页爬取的操作
'''




import json
import requests
#用多进程来抓取数据会更快
from multiprocessing import Pool
from requests.exceptions import RequestException
import re


def get_one_page(url):
   try:
       response = requests.get(url)
       if response.status_code == 200:
           return response.text
       return None
   except RequestException:
       return None


def parse_one_page(html):
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="([a-zA-z]+://[^\s]*)".*?name"><a.*?>(.*?)</a></p>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>',re.S)
    items = re.findall(pattern,html)
    for item in items:
        yield {#迭代器
            'index':item[0],
            'image':item[1],
            'title':item[2],
            'star' :item[3].strip(),
            'date' :item[4].strip(),
            'score':item[5]+item[6]
        }


def write_to_file(content):
    with open('result.txt','a',encoding='utf-8') as  f:
        f.write(json.dumps(content,ensure_ascii=False) + "\n" )
        f.close()


def main(offset):
    url = "https://maoyan.com/board/4" + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)



if __name__ == '__main__':
    pool = Pool()
    pool.map(main,[i*10 for i in range(10)])