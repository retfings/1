import multiprocessing
from bs4 import BeautifulSoup
import requests
from copy import deepcopy
import requests
import traceback
import concurrent.futures

key_words = ['Gravity+field+modeling',
            'Geostatistics+in+exploration',
            'Neutron+lifetime+log',
             'Fracturing+construction',
             'Petroleum+economics',
             'Petroleum+policies+and+management',
             'Stratigraphic+division+and+correlation',
             'Oil+development+project',
             'Gravity+data+reduction'
            ]
template = {
    'name':'',
    'author':'',
    
    'year':'',
    'link':''

}


lock = multiprocessing.Lock()

# import pymysql
# from pymysql import pool

# # 创建连接池
# def create_conn_pool():
#   conn_pool = pool.SimpleConnectionPool(
#     5, # 最少连接数
#     10, # 最多连接数
#     host="localhost",
#     database="local_mysql",
#     user="root",
#     password="091314"
#   )
#   return conn_pool

# conn_pool = create_conn_pool()


# def insert_to_record(name, author, publisher, year, language, pages, size, ext, link):
#     try:
#         # 获取游标
#         conn = conn_pool.getconn()
#         cur = conn.cursor()
#         # 执行SQL语句插入一条记录到record表中
#         query = f"INSERT INTO books (name, author, publisher, year, language, pages, size, ext, link) VALUES ('{name}', '{author}', '{publisher}', '{year}', '{language}', '{pages}', '{size}', '{ext}', '{link}')"
#         cur.execute(query)
#         # 提交事务
#         conn.commit()
#         # 关闭游标和连接
#         conn_pool.putconn(conn)
#         return True
#     except (Exception, psycopg2.DatabaseError) as error:
#         print(error)
#         return False



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
    proxy = get_proxy().get("proxy")
    while retry_count > 0:
        try:
            html = requests.get(url, headers=headers, proxies={"http": "http://{}".format(proxy)}).text
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
        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__)
            retry_count -= 1
    # 删除代理池中代理
    print("烂代理：" + str(proxy))
    delete_proxy(proxy)
    return None



def getHtml(url):
    # ....
    retry_count = 5
    proxy = get_proxy().get("proxy")
    while retry_count > 0:
        try:
            html = requests.get(url, headers=headers, proxies={"http": "http://{}".format(proxy)})
            if html is None:
                return
            return html.text
        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__)
            retry_count -= 1
    # 删除代理池中代理
    print("烂代理：" + str(proxy))
    delete_proxy(proxy)
    return None

def scrapy(keyword):
    result = []
    base_url = 'https://libgen.gs/index.php?req='+str(keyword)+'&topics%5B%5D=l&curtab=f&order=&ordermode=desc&filesuns=all&page='
    for i in range(100):
        url = base_url + str(i+1)
        print("scrapying the url:"+str(url)+"……")
        try:
            elem = getElem(url)
            if elem is None:
                return
            for ele in elem:#每本书
                book = deepcopy(template)
                info = ele.find_all("td")
                tag_a = None
                try:
                    test_XXXXX = tag_a
                    tag_a = info[0].find_all("a")
                    tag_a = tag_a[1]
                except:
                    test_XXXXX = tag_a
                    tag_a = info[0].find("a")
                name = tag_a.text
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


                text = getHtml(link)
                soup = BeautifulSoup(text,'html.parser')
                soup = soup.find("table")
                link = soup.find("a").get("href")
                book['link'] = 'https://libgen.rocks/' + link
                result.append(book)
                print(result)
                print(book["link"])
        except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                print("no page,drump")
                break
    return result


def get_task_ids(process_id):
    res = []
    tmp = process_id
    res.append(tmp)
    while tmp + 8 < len(key_words):
        tmp = tmp + 8
        res.append(tmp)
    return res

def run(chunk):
    print("chunk: " + str(chunk))
    for i in chunk:
        key_word = key_words[i]
        print("任务开始执行")
        result = scrapy(key_word)
        print(f"result: {result}")
        print("准备写数据库")
        if result is None:
            continue
        # print("result: " + str(result))
        print("开始写数据库")
        for row in result:
            print("row: " + str(row))
            # insert_to_record(row[0], row[1], row[2],row[3],row[4],row[5],row[6],row[7],row[8])

if __name__ == '__main__':
    thread_ids = []
    for i in range(0, 9):
        thread_ids.append(get_task_ids(i))
    # 启动多线程，每个线程处理一个子列表
    num_threads = 2
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        for chunk in thread_ids:
            print("提交一个任务： " + str(chunk))
            executor.submit(run, chunk)
