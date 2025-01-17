import requests
from bs4 import BeautifulSoup
import os
import threading

# 创建papers文件夹用于保存文献
path = "./papers/"
if not os.path.exists(path):
    os.mkdir(path)

# 请求头
head = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36"
}

# 下载文献的函数
def download_paper(doi):
    # 拼接Sci-Hub链接
    url = "https://www.sci-hub.ren/" + doi + "#"
    
    try:
        download_url = ""
        
        # 发送HTTP请求并解析HTML页面
        r = requests.get(url, headers=head)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        
        # 解析得到文献下载链接
        if soup.iframe == None:
            download_url = "https:" + soup.embed.attrs["src"]
        else:
            download_url = soup.iframe.attrs["src"]
        
        # 下载文献并保存到文件
        print(doi + "\t正在下载\n下载链接为\t" + download_url)
        download_r = requests.get(download_url, headers=head)
        download_r.raise_for_status()
        with open(path + doi.replace("/", "_") + ".pdf", "wb+") as temp:
            temp.write(download_r.content)

        print(doi + "\t文献下载成功.\n")

    # 下载失败时记录错误信息
    except Exception as e:
        with open("error.log", "a+") as error:
            error.write(doi + "\t下载失败!\n")
            if download_url.startswith("https://"):
                error.write("下载url链接为: " + download_url + "\n")
            error.write(str(e) + "\n\n")

# 打开包含doi号的txt文件
def run_from_doi_file():
    with open(path + "doi.txt", "r", encoding="utf-8") as f:
        # 遍历读取doi号，并启动多线程下载文献
        threads = []
        for line in f:
            doi = line.strip()
            t = threading.Thread(target=download_paper, args=(doi,))
            threads.append(t)
        
        # 启动所有线程
        for t in threads:
            t.start()

        # 等待所有线程完成
        for t in threads:
            t.join()

if __name__ == "__main__":
    download_paper('10.1038/s41524-017-0032-0')