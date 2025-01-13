# pip install trafilatura
# 使用示例:
# python
from trafilatura import fetch_url, extract
# html = fetch_url('http://www.ime.cas.cn/icac/learning/learning_2/201901/t20190121_5232288.html')

# http://www.ime.cas.cn/icac/learning/learning_2/201903/t20190314_5255072.html

html = fetch_url('https://www.eet-china.com/mp/a335715.html')
content = extract(html)
print(content)