import requests
# https://github.com/jhao104/proxy_pool
import requests

def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").json()

def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))
# 测试目标 URL
test_url = "http://httpbin.org/ip"

def getHtml():
    # ....
    retry_count = 5
    proxy = get_proxy().get("proxy")
    print(f"use:{proxy}")
    while retry_count > 0:
        try:
            html = requests.get(test_url, proxies={"http": "http://{}".format(proxy)})
            # 使用代理访问
            return html
        except Exception:
            retry_count -= 1
    # 删除代理池中代理
    delete_proxy(proxy)
    return None
print(getHtml().content)
# 遍历代理进行测试
# for proxy in proxies:
#     protocol = "http" if proxy["protocol"] == 2 else "https"
#     proxy_url = f"{protocol}://{proxy['ip']}:{proxy['port']}"
#     print(proxy_url)
#     proxies_dict = {
#         "http": proxy_url,
#         "https": proxy_url
#     }
#     try:
#         print(f"Testing proxy: {proxy_url}")
#         response = requests.get(test_url, proxies=proxies_dict, timeout=5,verify=False)
#         print(f"Response: {response.json()}\n")
#     except requests.exceptions.RequestException as e:
#         print(f"Failed to connect using proxy {proxy_url}: {e}\n")
