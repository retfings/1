import asyncio
import json
from crawl4ai import AsyncWebCrawler, CacheMode  
import os
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy

def save_markdown_to_file(url, markdown_content):

    filename = os.path.basename(url).replace(":", "_").replace("/", "_") + ".txt"
    filepath = os.path.join("markdown_files", filename)  
    os.makedirs(os.path.dirname(filepath), exist_ok=True)  
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(markdown_content)
    print(f"Saved Markdown for {url} to {filepath}")
    

def load_json(path):
    try:
        with open(path, encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading JSON: {e}")
        return []

def save_json(path, obj):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=4)

DOWNLOADED_FILE = 'downloaded.json'
downloaded = set(load_json(DOWNLOADED_FILE))  
print(f"downloaded count: {len(downloaded)}")
    # Define the extraction schema

# Create the extraction strategy

async def fetch_page(crawler:AsyncWebCrawler, url:str,schema:dict):
    
    extraction_strategy = JsonCssExtractionStrategy(schema, verbose=True)
    
    import time
    time.sleep(3)
    # if url in downloaded:
    #     print(f"Skipping already downloaded URL: {url}")
    #     return None
    
    downloaded.add(url)  
    save_json(DOWNLOADED_FILE, list(downloaded))  

    try:
        result = await crawler.arun(
            url=url,
            extraction_strategy=extraction_strategy
                                    )
        
        assert result.success, "Failed to crawl the page"
        
        
        from datetime import datetime
        
        timestamp = datetime.now().timestamp()

        save_json("schama-"+str(timestamp),result.extracted_content)
        
        # print(result.extracted_content)  

        # internal_links = result.links.get("internal", [])  
        # for link in internal_links:
        #     href = link.get('href')
        #     if href:
        #         await fetch_page(crawler, href)  
    except Exception as e:
        print(f"Error fetching URL {url}: {e}")

async def main(url:str,scheme:dict):
    # https://www.eet-china.com/mp/a335715.html
    # http://www.ime.cas.cn/icac/learning/learning_2/201901/t20190121_5232288.html
    # start_url = "http://www.ime.cas.cn/icac/learning/learning_2/201901/t20190121_5232288.html"
    async with AsyncWebCrawler(verbose=True) as crawler:
        await fetch_page(crawler, url,scheme)

if __name__ == "__main__":
    url = "https://www.eet-china.com/mp/a335715.html"
    
    from web.eetchina import Eetchina
    
    asyncio.run(main(url,Eetchina.get_schema()))
    
    print(f"crawl: {url}")


    
    # url = "http://www.ime.cas.cn/icac/learning/learning_2/201901/t20190121_5232288.html"
    # from web.imecas import Imecas
    
    # asyncio.run(main(url,Imecas.get_schema()))