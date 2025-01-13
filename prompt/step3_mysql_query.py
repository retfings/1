import pandas as pd
from sqlalchemy import create_engine

# 读取 Excel 文件
excel_file = 'data_with_columns.xlsx'
df_config = pd.read_excel(excel_file)

# 数据库连接信息
db_url = 'mysql+pymysql://root@10.10.104.25:9030/cdm'
engine = create_engine(db_url)

# 遍历 Excel 文件中的每一行
for index, row in df_config.iterrows():
    table_name = row['数据表名']  # 假设 Excel 文件中有一列名为 '数据库表名'
    keyword_columns = row['字段名']  # 假设 Excel 文件中有一列名为 '字段名'

    for key in keyword_columns.split('、'):

        # 检查字段名是否为空
        if pd.isna(keyword_columns) or keyword_columns.strip() == "":
            # print(f"第 {index + 1} 行：字段名为空，跳过该行")
            continue

        # 构建 SQL 查询（查询字段名不为空的记录）
        query = f"SELECT * FROM {table_name} WHERE {key} = 'A29T216#01'"

        # 执行查询并获取数据
        try:
            df_result = pd.read_sql(query, engine)
            if len(df_result) != 0:
                
                print(df_result)
                exit()
            # # 保存结果到 Excel 文件
            # output_file = f"{table_name}_{keyword_column}_not_null.xlsx"
            # df_result.to_excel(output_file, index=False)
            # print(f"数据已保存到 {output_file}")
        except Exception as e:
            # print(f"查询表 {table_name} 时出错：{e}")
            pass