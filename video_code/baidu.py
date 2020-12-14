import requests
from bs4 import BeautifulSoup

if __name__ == "__main__":
    # 你要搜的东西
    keyword = 'python3'
    # 第n页
    pn = 1
    url = 'https://www.baidu.com/s'
    params = {"wd": keyword, "pn": (pn-1)*10}
    ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    headers = {"User-Agent": ua}
    response = requests.get(url, params=params, headers=headers)
    text = response.text.replace('\n', '')
    soup = BeautifulSoup(text, features="lxml")
    link_title = soup.findAll('h3')
    for link in soup.findAll('a'):
        if link.parent in link_title:
            print(link.text+"\n"+link.attrs['href'])
