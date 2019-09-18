import re
import requests
from requests.exceptions import RequestException


def get_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def parse_page(html):
    pattern = re.compile('<dd>.*?data-val="{(.*?)}">.*?poster-default.*?data-src="([a-zA-z]+://[^\s]*).*?<a href.*?movieId.*?">(.*?)</a>.*?integer">(.*?)</i><i.*?fraction">(.*?)</i></div>',re.S)
    page_info = re.findall(pattern,html)
    for item in page_info:
        yield {
            'movieID':item[0][8:],
            'image'  :item[1],
            'title'  :item[2],
            'score'  :item[3]+item[4]
        }

def main():
    url = "https://maoyan.com/films"
    html =  get_page(url)
    parse_page(html)
    for item in parse_page(html):
        print(item)

if __name__ == "__main__":
    main()
