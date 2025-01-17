import pandas as pd


# Load the files
file_A_path = "快捷查询维度说明_processed_20250113_from_tianyi.csv"
file_B_path = "distinct_values_output.xlsx"

# Load A file (CSV)
df_A = pd.read_csv(file_A_path)

# Load B file (Excel)
df_B = pd.read_excel(file_B_path)

# Ensure '查询条件' is treated as a string to avoid errors with missing values
df_A['查询条件'] = df_A['查询条件'].astype(str)

# Updating the '查询条件' column in A using the values from B where 数据表名 and 表名 match
for index_B, row_B in df_B.iterrows():
    table_name = row_B['表名']
    field_name = row_B['字段名']
    distinct_values = row_B['不同值']
    
    # Update the matching rows in A
    for index_A, row_A in df_A.iterrows():
        if row_A['数据表名'] == table_name and field_name in row_A['查询条件']:
            # Modify the 查询条件 by replacing the field with the values
            updated_condition = row_A['查询条件'].replace(field_name, f"{field_name}({distinct_values})")
            df_A.at[index_A, '查询条件'] = updated_condition


df_A.to_csv("带字段名_20250114v1.csv")