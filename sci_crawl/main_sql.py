import json
import pandas as pd
import mysql.connector

# # 1. 读取 key_en.json 文件
# with open('key_en.json', 'r') as file:
#     data = json.load(file)

# 2. 连接数据库
conn = mysql.connector.connect(
    host="10.10.100.15",
    user="root",
    password="Zeta@2025",
    database="scihub",
    ssl_disabled=True  # 禁用 SSL
)

# 3. 查询数据
query = "SELECT DOI, DOI2, title FROM scimag"
df = pd.read_sql(query, conn)

# 4. 导出到 CSV
df.to_csv('output.csv', index=False)

# 关闭数据库连接
conn.close()