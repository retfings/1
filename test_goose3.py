from goose3 import Goose
from goose3.text import StopWordsChinese
# 初始化，设置中文分词
g = Goose({'stopwords_class': StopWordsChinese})
# 文章地址
url = 'http://www.ime.cas.cn/icac/learning/learning_2/201903/t20190314_5255072.html'
# 获取文章内容
article = g.extract(url=url)
# 标题
print('标题：', article.title)
# 显示正文
print('正文：',article.cleaned_text)

