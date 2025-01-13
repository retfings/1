from sqlalchemy import create_engine, inspect
import pandas as pd

# 数据库连接信息
db_url = 'mysql+pymysql://root@10.10.104.25:9030/cdm'
engine = create_engine(db_url)

# 创建 Inspector 对象
inspector = inspect(engine)

# 获取所有表名
table_names = inspector.get_table_names()

# 创建一个空列表，用于存储表名和字段名
data = []

# 遍历表名并获取字段
for table_name in table_names:
    columns = inspector.get_columns(table_name)
    # 将字段名用 '、' 分割
    column_names = '、'.join([column['name'] for column in columns])
    # 将表名和字段名组合为一行数据
    data.append([table_name, column_names])

# 将数据转换为 DataFrame
df = pd.DataFrame(data, columns=['表名', '字段名'])

# 保存到 CSV 文件
df.to_csv('table_and_columns.csv', index=False, encoding='utf-8')

print("表名和字段已保存到 table_and_columns.csv")