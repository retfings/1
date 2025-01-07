from gne import GeneralNewsExtractor
extractor = GeneralNewsExtractor()
import requests
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Cookie': 'Secure',
    'Pragma': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0'
}
def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").json()

def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))
    
    

from datetime import datetime
import json
def save_json(path,obj):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=4)
import json
def load_json(path):
    try:
        with open(path, encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading JSON: {e}")
        return [] 

import os

os.makedirs('data',exist_ok=True)    
DOWNLOADED_FILE = 'downloaded.json'
downloaded = list(set(load_json(DOWNLOADED_FILE)))  
from retrying import retry

# @retry(stop_max_attempt_number=3, wait_fixed=1000)
def request(url):
    response = requests.get(url,headers=headers)
    response.raise_for_status()
    # response = requests.get("http://www.ime.cas.cn/icac/learning/learning_2/201901/t20190121_5232288.html",headers=headers)
    # print(response.text)
    content = response.content.decode('utf-8')
    # print(content)
    result = extractor.extract(content)
    timestamp = datetime.now().timestamp()

    save_path = 'data/'+str(timestamp)
    save_json(save_path,result)
    print(f"save : {save_path}")
    downloaded.append(url)  
    save_json(DOWNLOADED_FILE, list(downloaded))  
    import time
    # time.sleep(3)
    # print(f"parse {url}")
    # print("sleep 3s")

from search import search_by_google
from urllib.parse import urlparse
def skip(path):
    
    # 跳过已经下载的网站
    if path in downloaded:
        return True
    parsed_url = urlparse(path) 
    path = parsed_url.path
    
    # 如果是网站跟目录不爬取
    if len(path) == 1:
        return True
    if  path.endswith(".pdf") or \
        path.endswith(".PDF") or \
        path.endswith(".doc") or \
        path.endswith(".DOC") or \
        path.endswith(".docx") :
        return True

    # # 跳过一些文档不行的网站
    # skips = [
    #     "https://www.st.com.cn/content/st_com/zh/browse/product-portfolio.html",
    #     "https://www.mouser.cn/c/semiconductors/"
    # ]
    # for skip in skips:
    #     if path in skip:
    #         print(f"skip: {url}")
    #         return True
    return False

def load_and_process_data(data):
    for process_group in data["Process Group"]:
        group_name = process_group["name"]
        yield group_name
        # print(f"Process Group: {group_name}")
        
        for process_module in process_group["Process Module"]:
            module_name = process_module["name"]
            yield module_name
            # print(f"  Process Module: {module_name}")
            
            for process_unit in process_module["Process Unit"]:
                yield process_unit
                # print(f"    Process Unit: {process_unit}")
        # print("\n")  # 添加空行分隔不同的Process Group




if __name__ == "__main__":
    lang = 'cn' if True else 'en'
    site = 'patents.google.com' if False else ''
    num_results = 10
    start = 20
    # open('start.txt')
    for key in load_and_process_data(load_json(f'key_{lang}.json')):

        searchkey = f'{key}'  if lang == 'cn' else f'Semiconductor Process Ontology {key}'
        # print(f"searchkey {searchkey}")
        proxy = f'http://{get_proxy().get("proxy")}' if False else ''
        urls = []
        # for url in search_by_google(searchkey,site=site,proxy=proxy,num_results=num_results,start=start):
        
        # file = deduplication.url.txt
        file_urls = "url_en.txt"
        with open(file_urls) as f:
            urls = f.readlines()

            
        print(f"load {len(urls)} urls")
        for url in urls:
            url = url.split(",")[0]
            if skip(url.strip()):
                print(f"skip url {url}")
                continue
            
            
            try:
                request(url.strip())
                print(f"crawl {url}")
            except Exception as e:
                print(url)
                print(e)
        # exit(0)
        
        

