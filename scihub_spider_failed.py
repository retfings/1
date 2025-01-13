import multiprocessing

import pandas as pd
import time
import os
import random
import csv
import re

import traceback
import requests as requests
from bs4 import BeautifulSoup

import pymysql
from pymysql import pool
# 创建连接池
# def create_conn_pool():
#     conn_pool = psycopg2.pool.SimpleConnectionPool(
#         5,  # 最少连接数
#         10,  # 最多连接数
#         host="localhost",
#         database="postgres",
#         user="postgres",
#         password="12345678"
#     )
#     return conn_pool
# 创建连接池
def create_conn_pool():
  conn_pool = pool.SimpleConnectionPool(
    5, # 最少连接数
    10, # 最多连接数
    host="localhost",
    database="local_mysql",
    user="root",
    password="091314"
  )
  return conn_pool

conn_pool = create_conn_pool()


tmp_lst = []
with open("/Users/aboysky/Downloads/scihub_final.csv") as f:
    file = csv.reader(f)
    for row in file:
        tmp_lst.append(row)
table = pd.DataFrame(tmp_lst[1:], columns=tmp_lst[0])
table.dropna(axis=0,how='any')
dois = table['DOI'].copy(deep=True)
for i in dois.index:
    dois[i] = str(dois[i])
finished = [0 for i in range(len(dois))]
years = table['year']
title = table['title'].copy(deep=True)


def insert_to_record(file_name):
  try:
    # 获取游标
    conn = conn_pool.get_connection()
    cur = conn.cursor()
    # 执行SQL语句插入一条记录到record表中
    query = f"INSERT INTO record (file_name, status) VALUES ('{file_name}', 1)"
    cur.execute(query)
    # 提交事务
    conn.commit()
    # 关闭游标和连接
    cur.close()
    conn_pool.put_connection(conn)
    return True
  except (Exception, pymysql.DatabaseError) as error:
    print(error)
    return False



def safe_filename(s):
    """
    Convert any string to a safe, usable filename on macOS.
    """
    # Replace special characters with hyphens
    s = re.sub(r'[^\w\-\.]', '-', s)
    # Remove any runs of periods or hyphens
    s = re.sub(r'[\-\.]+', '-', s)
    # Truncate filename if it's too long
    basename, extension = os.path.splitext(s)
    basename = basename[:240]
    s = basename + extension
    # Return the modified string
    return s
def rename_file(dois, finished, auths, years, i):
    time.sleep(1)
    path = '/Users/aboysky/scrapy/scihub/'
    dir_list = os.listdir(path)
    if len(dir_list)>0:
        found = 0
        for file in dir_list:
            if file[0:3]!='No_':
                found = 1
                break

        if found==0: #when didn't get the "save" button
            print('download failed.    index = '+str(i)+'    doi = '+dois[i])
        else: #when we get a new file
            l = file.split('.')
            if l[len(l)-1] != "pdf": #when the file was half downloaded
                print('download incomplete.    index = '+str(i)+'    doi = '+dois[i])
            else:
                old = path+ file
                auth = str(auths[i])
                try:
                    year = str(int(years[i]))
                except:
                    year = str(years[i])
                index = [str(i//100), str((i%100)//10), str(i%10)]

                new = path+ 'No_' +index[0]+index[1]+index[2]+'_' +auth+'_'+year+'.pdf'
                os.rename(old, new)
                finished[i] = 1

def scihub_get(dois, i):
    try:
        scihub = ['https://sci-hub.ru/', 'https://sci-hub.st/', 'https://sci-hub.se/']
        root = scihub[random.randint(0,2)]
        # search by doi
        doi = dois[i]
        url = root + doi
        # 请求网页并获取 HTML 内容
        response = requests.get(url)
        html = response.text
        # 解析 HTML 内容，查找下载按钮的链接
        soup = BeautifulSoup(html, 'html.parser')
        download_btn = soup.select_one('#buttons button')
        if not download_btn or not download_btn['onclick'] or not download_btn['onclick'].split("'") or not download_btn['onclick'].split("'")[1]:
            return False
        download_url = download_btn['onclick'].split("'")[1]
        download_url = root[:-1] + download_url
        # 使用 requests 库下载 PDF 文件
        response = requests.get(download_url)
        base_dir = '/Users/aboysky/scrapy/scihub/'
        tmp_years = years[i]
        if tmp_years is None:
            tmp_years = ''
        tmp_title = title[i]
        if tmp_title is None:
            tmp_filename = download_url.split('/')[-1]
            tmp_filename = tmp_filename.split('?')[0]
            tmp_title = tmp_filename
        filename = str(tmp_title) + str(tmp_years) + '.pdf'
        filename = safe_filename(filename)
        with open(base_dir + filename, 'wb') as f:
            f.write(response.content)
            print(f'download {filename} successfully!')
            insert_to_record(filename)
            return True
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return False


def article_get(dois, finished, auths, years, i):
    # visit scihub
    if dois[i] == 'nan':
        print('doi missing. index = ' + str(i))
    else:
        if scihub_get(dois, i):
            # rename
            rename_file(dois, finished, auths, years, i)

def run(chunk):
    for i in chunk:  # len(dois)):
        scihub_get(dois, i)

if __name__ == '__main__':
    # 设置进程池
    tasks = list(range(len(dois)))
    # 将任务列表拆分成 8 个子列表
    chunk_size = len(dois) // 8
    task_chunks = [tasks[i:i + chunk_size] for i in range(0, len(tasks), chunk_size)]

    # 启动多进程，每个进程处理一个子列表
    num_processes = 8
    with multiprocessing.Pool(processes=num_processes) as pool:
        results = [pool.apply_async(run, args=(chunk,)) for chunk in task_chunks]
        pool.close()
        pool.join()