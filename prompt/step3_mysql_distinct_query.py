import pandas as pd
from sqlalchemy import create_engine
from tqdm import tqdm
# 读取 Excel 文件
excel_file = 'data_with_columns.xlsx'
df_config = pd.read_excel(excel_file)

# 数据库连接信息
db_url = 'mysql+pymysql://root@10.10.104.25:9030/cdm'
engine = create_engine(db_url)

# 创建一个空的 DataFrame 用于保存结果
result_data = []

# 遍历 Excel 文件中的每一行
for index, row in tqdm(df_config.iterrows()):
    table_name = row['数据表名']  # 假设 Excel 文件中有一列名为 '数据表名'
    keyword_columns = row['字段名']  # 假设 Excel 文件中有一列名为 '字段名'

    # 检查字段名是否为空
    if pd.isna(keyword_columns) or keyword_columns.strip() == "":
        print(f"第 {index + 1} 行：字段名为空，跳过该行")
        continue

    # 遍历每个字段名（以 '、' 分隔）
    for key in keyword_columns.split('、'):
        # 检查字段名是否为空
        if pd.isna(key) or key.strip() == "":
            continue


        # if "bin" in key:
        #     continue

        # 查询该字段的不同值
        distinct_query = f"SELECT DISTINCT {key} FROM {table_name}"
        
        print(f"SQL:{distinct_query}")
        
        try:
            df_distinct = pd.read_sql(distinct_query, engine)
            
            # 将不同值用 ; 分隔
            distinct_values = ';'.join(df_distinct[key].astype(str).tolist())
            
            # 将结果添加到 result_data
            result_data.append({
                '表名': table_name,
                '字段名': key,
                '不同值': distinct_values
            })
        except Exception as e:
            print(f"查询表 {table_name} 中字段 {key} 时出错：{e}")
            

# 将结果保存到 DataFrame
df_result = pd.DataFrame(result_data, columns=['表名', '字段名', '不同值'])

# 保存到 Excel 文件
output_file = 'distinct_values_output.xlsx'
df_result.to_excel(output_file, index=False)
print(f"结果已保存到 {output_file}")