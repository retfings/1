import redis

def test_redis_connection():
    try:
        # 连接到Redis服务器
        client = redis.Redis(host='localhost', port=6379, db=0,password='infini_rag_flow')

        # 测试连接
        if client.ping():
            print("成功连接到Redis服务器！")

        # 设置键值对
        client.set('test_key', 'Hello Redis!')

        # 获取键的值
        value = client.get('test_key')
        print(f"test_key的值: {value.decode('utf-8')}")

        # 删除键
        client.delete('test_key')
        print("测试完成，test_key已删除。")

    except Exception as e:
        print(f"发生错误: {e}")

def list_all_keys():
    try:
        # 连接到Redis服务器
        client = redis.Redis(host='localhost', port=6379, db=0,password='infini_rag_flow')

        # 获取所有键
        keys = client.keys('*')

        if keys:
            print("Redis中存在的键：")
            for key in keys:
                print(key.decode('utf-8'))
        else:
            print("Redis中没有键。")

    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    list_all_keys()
