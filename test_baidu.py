

import requests


data = requests.get("https://www.bing.com/search?q=baidu+search+api")
print(data.content)