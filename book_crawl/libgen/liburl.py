from bs4 import BeautifulSoup
import requests
from copy import deepcopy
import csv
import random


key_words = ['semiconductor']
template = {
    'name':'',
    'author':'',
    'year':'',
    'link':''
}



def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").json()

def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Cache-Control': 'no-cache' ,
    'Connection': 'keep-alive' ,

    'Cookie': 'objects=f%7Ce%7Cs%7Ca%7Cp%7Cw; curtab=f; PHPSESSID=iu33bopvk1val3kshn3frcmjah; columns=t%7Ca%7Cs%7Cy%7Cp%7Ci; topics=l%7Cc%7Cf%7Ca%7Cm%7Cr%7Cs' ,

    'Pragma': 'no-cache' ,

    'Referer': 'https://libgen.li/?semiconductor' ,

    'Sec-Fetch-Dest': 'document' ,

    'Sec-Fetch-Mode': 'navigate' ,

    'Sec-Fetch-Site': 'same-origin' ,

    'Sec-Fetch-User': '?1' ,

    'Upgrade-Insecure-Requests': '1' ,

    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.54' ,

    'sec-ch-ua': 'Microsoft Edge";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': 'macOS'
    }
def getElem(url):
    # ....
    retry_count = 5
    # proxy = get_proxy().get("proxy")
    while retry_count > 0:
        try:
            # , proxies={"http": "http://{}".format(proxy)}
            html = requests.get(url, headers=headers).text
            # 使用代理访问
            if html is None:
                continue
            soup = BeautifulSoup(html,'html.parser')
            soup = soup.find("table",{'class':'table table-striped'})
            if soup is None:
                print("url: " + url + " not exist table")
                return
            soup = soup.find("tbody")
            if soup is None:
                print("url: " + url + " not exist tbody")
                return
            elem = soup.find_all('tr')
            if elem is None:
                print("url: " + url + " not exist tr")
            return elem
        except:
            retry_count -= 1
    # 删除代理池中代理
    # print("烂代理：" + str(proxy))
    # delete_proxy(proxy)
    return None



def getHtml(url):
    # ....
    retry_count = 5
    # proxy = get_proxy().get("proxy")
    while retry_count > 0:
        try:
            # , proxies={"http": "http://{}".format(proxy)}
            html = requests.get(url, headers=headers)
            if html is None:
                return
            return html.text
        except Exception as e:
            retry_count -= 1
    # 删除代理池中代理
    # print("烂代理：" + str(proxy))
    # delete_proxy(proxy)
    return None

def scrapy(keyword):
    result = []
    base_url = 'https://libgen.gs/index.php?req='+str(keyword)+'&topics%5B%5D=l&curtab=f&order=&ordermode=desc&filesuns=all&page='
    for i in range(100):
        url = base_url + str(i+1)
        print("scrapying the url:"+str(url))
        try:
            elem = getElem(url)
            if elem is None:
                return
            for ele in elem:#每本书
                book = deepcopy(template)
                info = ele.find_all("td")
                # tag_a = None
                # try:
                #     test_XXXXX = tag_a
                #     tag_a = info[0].find_all("a")
                #     tag_a = tag_a[1]
                # except:
                #     test_XXXXX = tag_a
                #     tag_a = info[0].find("a")
                name = info[0].find("a").text
                author = info[1].text
                publisher = info[2].text
                year = info[3].text
                language = info[4].text
                pages = info[5].text
                size = info[6].find("a").text
                ext = info[7].text
                link = info[8].find("a").get("href")

                book['name'] = str(name)
                book['author'] = str(author)
                book['publisher'] = str(publisher)
                book['year'] = str(year)
                book['language'] = str(language)
                book['pages'] = str(pages)
                book['size'] = str(size)
                book['ext'] = str(ext)

# https://libgen.gs/ads01ce4e6980d28a8bee3a296ece7bc6148KC775UM
# -> https://libgen.gs/get.php?md5=01ce4e6980d28a8bee3a296ece7bc614&key=2329JCRASHG20OF2
                url = 'https://libgen.gs/' + link
                # text = getHtml(link)
                # soup = BeautifulSoup(text,'html.parser')
                # soup = soup.find("table")
                # link = soup.find("a").get("href")
                # book['link'] = 'https://libgen.rocks/' + link
                book['link'] = url
                
                result.append(book)
        except :
                print("no page,drump")
                break
    return result




def main():
        
    import pandas as pd

    # 创建一个空的 DataFrame，指定列名
    columns = ['name', 'author', 'publisher', 'year', 'language', 'pages', 'size', 'ext', 'link']
    df = pd.DataFrame(columns=columns)

    # 遍历 key_words，获取结果并填充 DataFrame
    for key_word in key_words:
        print(f"key_word:{key_word}")
        result = scrapy(key_word)
        print(f"result:{key_word}")
        
        if result:
            # 将结果添加到 DataFrame
            temp_df = pd.DataFrame(result)  # 假设 result 是一个列表字典格式
            df = pd.concat([df, temp_df], ignore_index=True)
        else:
            print(f"No results found for key_word: {key_word}")

    # 将 DataFrame 保存到 CSV 文件中
    df.to_csv('new_book_list.csv', index=False, encoding='utf-8')


if __name__ == "__main__":
    main()