# 导入BaiduSpider
from baiduspider import BaiduSpider
from pprint import pprint

# 实例化BaiduSpider
spider = BaiduSpider()
res = spider.search_web(query='Python')
# 搜索网页
pprint(res)