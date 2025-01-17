from scihub_cn.scihub import SciHub
import time
sh = SciHub()
import urllib3
# Ensure certificate verification is enabled
urllib3.disable_warnings() 
# 设置is_translate_title可将paper's title进行翻译后下载存储
for line in open('dois.txt').readlines():
    try:
        time.sleep(5)
        sh.download({"doi": line})
    except Exception as e:
        print(e)