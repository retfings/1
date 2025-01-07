from googlesearch import search

    
import time
from typing import List
# from googlesearch import search


from time import sleep
from bs4 import BeautifulSoup
from requests import get
            
import random


def get_useragent():
    return random.choice(_useragent_list)


_useragent_list = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.62',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0'
]


def _req(term, results, lang, start, proxies, timeout, safe, ssl_verify, region):
    resp = get(
        url=f"https://www.google.com/search",
        
        headers={
            "User-Agent": get_useragent()
        },
        params={
            "q": term,
            # "num": results + 2,  # Prevents multiple requests
            # "hl": lang,
            "start": start,
            # "safe": safe,
            # "gl": region,
        },
        proxies=proxies,
        timeout=timeout,
        verify=ssl_verify,
    )
    resp.raise_for_status()
    return resp


class SearchResult:
    def __init__(self, url, title, description):
        self.url = url
        self.title = title
        self.description = description

    def __repr__(self):
        return f"SearchResult(url={self.url}, title={self.title}, description={self.description})"

def search(term, num_results=10, lang="en", proxy=None, advanced=False, sleep_interval=0, timeout=5, safe="active", ssl_verify=None, region=None,start=0):
    """Search the Google search engine"""

    # Proxy setup
    proxies = {"https": proxy, "http": proxy} if proxy and (proxy.startswith("https") or proxy.startswith("http")) else None

    # start = 0
    fetched_results = 0  # Keep track of the total fetched results

    while fetched_results < num_results:
        # Send request
        resp = _req(term, num_results - start,
                    lang, start, proxies, timeout, safe, ssl_verify, region)

        # Parse
        soup = BeautifulSoup(resp.text, "html.parser")
        result_block = soup.find_all("div", attrs={"class": "g"})
        new_results = 0  # Keep track of new results in this iteration

        for result in result_block:
            # Find link, title, description
            link = result.find("a", href=True)
            title = result.find("h3")
            description_box = result.find("div", {"style": "-webkit-line-clamp:2"})

            if link and title and description_box:
                description = description_box.text
                fetched_results += 1
                new_results += 1
                if advanced:
                    yield SearchResult(link["href"], title.text, description)
                else:
                    yield link["href"]

            if fetched_results >= num_results:
                break  # Stop if we have fetched the desired number of results

        if new_results == 0:
            #If you want to have printed to your screen that the desired amount of queries can not been fulfilled, uncomment the line below:
            #print(f"Only {fetched_results} results found for query requiring {num_results} results. Moving on to the next query.")
            break  # Break the loop if no new results were found in this iteration

        start += 10  # Prepare for the next set of results
        sleep(sleep_interval)



def search_by_google(keyword: str, site: str = '',proxy:str ='', lang: str = 'zh', retries: int = 3, delay: int = 5, start:int=0,**kwargs) -> List[str]:
    """
    Search by Google with retry mechanism.

    Args:
        keyword: Query keyword.
        site: Specific site to search within.
        lang: Query language.
        retries: Maximum number of retries on failure.
        delay: Delay between retries in seconds.
        **kwargs: Additional arguments for `googlesearch.search`.

    Returns:
        A list of URLs found in the search results.
    """
    attempt = 0
    while attempt < retries:
        try:
            # Construct the query string
            query = f"{keyword}" if site == '' else f"site:{site} {keyword}"
            # Call the search function
            res = [url for url in search(query, lang=lang,proxy=proxy,sleep_interval=2, start=start,**kwargs)]
            return res
        except TypeError as e:
            print("Ensure the correct arguments are passed to the 'search' function.")
            raise
        except Exception as e:
            attempt += 1
            print(f"Attempt {attempt} failed. Retrying in {delay} seconds... Error: {e}")
            time.sleep(delay)
    print(f"All {retries} attempts failed. Returning an empty list.")
    return []


def test_search_by_google():
    keyword = '半导体'
    site = ''
    num_results = 200
    print(search_by_google(keyword,site=site,num_results=num_results))
    
def load_and_process_data(data):
    for process_group in data["Process Group"]:
        group_name = process_group["name"]
        yield group_name
        # print(f"Process Group: {group_name}")
        try:
            for process_module in process_group["Process Module"]:
                module_name = process_module["name"]
                yield module_name
                # print(f"  Process Module: {module_name}")
                
                for process_unit in process_module["Process Unit"]:
                    yield process_unit
        except:
            pass
                
import json
def load_json(path):
    with open(path,encoding='utf-8') as f:
        return  json.load(f)    
import json
def save_json(path,obj):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=4)    
if __name__ == "__main__":
    lang = 'cn'
    crawl_count = 20000000000
    import pandas as pd 
    import os 
    
    if not os.path.exists('url.txt'):
        open("url.txt",'w')

    urls =  open("url.txt").readlines()
    crawl_key_count = {}

    import random
    dataset = list(load_and_process_data(load_json(f'key_{lang}.json')))

    
    
    for _ in range(50000):
        # if key not in ['SIC','DRAM','SRAM','HBM','etc']:
        #     continue
        key = f"'{random.choice(dataset)}' + '{random.choice(dataset)}'"
        
        for start in range(0, crawl_count, 10):
            print(f"page:{start}")
        # test_search_by_google()
            searchkey = f'{key}'  
            # searchkey = f'半导体工艺本体 {key}'  if lang == 'cn' else f'Semiconductor Process Ontology {key}' 
            print(searchkey)
            try:
                req = _req(searchkey,0,lang,start,None,3,'active',None,None)
                assert req.status_code == 200
            except Exception as e:
                print(e)
                continue
            soup = BeautifulSoup(req.text, "html.parser")
            result_block = soup.find_all("div", attrs={"class": "g"})
            hrefs = []
            for result in result_block:
                # Find link, title, description
                link = result.find("a", href=True)
                if link:
                    hrefs.append(link["href"])
            if len(hrefs) == 0:
                crawl_key_count[key] = start
                break
            
            
            
            from datetime import datetime
            # 获取当前日期
            current_date = datetime.now()
            # 格式化日期为 "vYYYYMMDD" 格式
            version_string = current_date.strftime("v%Y%m%d")
            
            save_json(f'key_count_stat_{lang}_{version_string}.json',crawl_key_count)
                     
            time.sleep(5)
            with open(f"url_{lang}_{version_string}.txt", 'a+',encoding='utf-8') as file:
                file.writelines(f'{url},{key}\n' for url in hrefs)
            print(f"len wirite {hrefs}")
