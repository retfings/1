from elasticsearch import Elasticsearch

# 使用用户名和密码进行认证
es = Elasticsearch(
    "http://localhost:9200",  # Elasticsearch 地址
    basic_auth=("elastic", "admines")  # 用户名和密码
)

# 检查连接是否成功
if es.ping():
    print("Connected to Elasticsearch!")
else:
    print("Could not connect to Elasticsearch.")
