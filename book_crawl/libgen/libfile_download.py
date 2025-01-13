
import requests
import pandas 
# 创建连接对象
import pymysql
# 创建连接池
import time
import traceback
import os 
import multiprocessing
import psycopg2
from psycopg2 import pool
import concurrent.futures

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

    'Upgrade-Insecure-Requests': '2' ,

    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.54' ,

    'sec-ch-ua': 'Microsoft Edge";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': 'macOS'
    }

def create_conn_pool():
    conn_pool = psycopg2.pool.SimpleConnectionPool(
        5,  # 最少连接数
        10,  # 最多连接数
        host="localhost",
        database="database",
        user="postgres",
        password="postgres"
    )
    return conn_pool
conn_pool = create_conn_pool()

conn = conn_pool.getconn()
# 创建游标对象
cursor = conn.cursor()
# 定义查询语句
query = 'SELECT name,ext,link FROM books_urldownload'
# 执行查询
cursor.execute(query)
# 获取查询结果
result = cursor.fetchall()
result = list(result)
res = []
for str in result:
    res.append([str[0],str[2],str[1]])

#创建连接池




def insert_to_record(file_name,conn):
    try:
        # 获取游标
        cur = conn.cursor()
        # 执行SQL语句插入一条记录到record表中
        query = f"INSERT INTO downloadedbooks  (name, status) VALUES ('{file_name}', 1)"
        cur.execute(query)
        # 提交事务
        conn.commit()
        # 关闭游标和连接
        cur.close()
        return True
    except (Exception, pymysql.DatabaseError) as error:
        print(error)
        return False
    
def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").json()

def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))

def get(sql):
    file_name = sql[0] +'.'+sql[2]
    # ....
    retry_count = 5
    proxy = get_proxy().get("proxy")
    while retry_count > 0:
        try:
            time.sleep(2)
            html = requests.get(sql[1],headers=headers,proxies={"http": "http://{}".format(proxy)},stream=True)
            # 使用代理访问
            if html is None:
                continue
            with html as response:
                response.raise_for_status()  # 触发 HTTPError，如果响应的状态码不好
                with open("/Users/tianyi/Downloads/libgenius/"+file_name, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            file.write(chunk)  
                # 判断下载请求是否完成
                if response.status_code == 200:
                    print('Download request is complete!')
                    insert_to_record(sql[0],conn)
                    return 
                else:
                    print('Download request failed!')
                    
        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__)
            retry_count -= 1
    # 删除代理池中代理
    print("烂代理")
    delete_proxy(proxy)
    return None

  

# for i in range(len(res)):
#     print(res[i])
#     get(res[i])

def run(chunk):
    print(chunk)
    for i in chunk:  # len(dois)):
        get(res[i])

if __name__ == '__main__':
    # 设置进程池
    tasks = list(range(len(res)))
    # 将任务列表拆分成 8 个子列表
    chunk_size = len(res) // 2
    task_chunks = [tasks[i:i + chunk_size] for i in range(0, len(tasks), chunk_size)]

    num_workers = 2 
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        for data in task_chunks:
            executor.submit(run, data)

        executor.shutdown()


    print('All tasks completed successfully!')
    # with multiprocessing.Pool(processes=num_processes) as pool:
    #     results = [pool.apply_async(run, args=(chunk,)) for chunk in task_chunks]
    #     pool.close()
    #     pool.join()