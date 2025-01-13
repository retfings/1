import pandas as pd

# 读取 data.xlsx 文件
data_df = pd.read_excel('data.xlsx')

# 读取 table_and_columns.csv 文件
table_columns_df = pd.read_csv('table_and_columns.csv')

# 创建一个字典，存储表名和字段名的映射关系
table_columns_dict = dict(zip(table_columns_df['表名'], table_columns_df['字段名']))

# 在 data.xlsx 中添加新列，存储对应的字段名
data_df['字段名'] = data_df['数据表名'].map(table_columns_dict)

# 保存修改后的 data.xlsx 文件
data_df.to_excel('data_with_columns.xlsx', index=False)

print("处理完成，结果已保存到 data_with_columns.xlsx")