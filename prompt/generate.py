
from openai import AsyncOpenAI,OpenAI
import json
import pandas as pd
client = OpenAI(
    api_key="sk-c765e87a50df47cfb82b0c16c6da0066", 
    base_url="https://api.deepseek.com"
)

df = pd.read_csv('快捷查询维度说明_processed_20250113_from_tianyi.csv')

results = []

for index,row in df.head(2).iterrows():
    print(row)
    continue
    data_type = row['Data Type']
    loader_level = row['Loader Level']
    table_name = row['数据表名']
    
    base_info = {
        "data_type": row['Data Type'],
        "loader_level": row['Loader Level'],
        "table_name": row['数据表名']
    }
    query = row['查询条件']
    # print(data_type)
    # print(loader_level)
    # print(table_name)
    # print(query)
    
    prompt = """
    目标：模拟用户生成问题。
    返回格式：json {questions:['question1','question2'...]}

    根据以下数据字段：
    - start_time（开始时间）
    - product_type（产品类型）
    - product_id（产品ID）
    - measure_stage（测量阶段）
    - lot_id（批次ID）
    - wafer_id（晶圆ID）
    - parameter_name（参数名称）
    - lot_type（批次类型）
    - chart_type（图表类型）
    - measure_step_seq（测量步骤序列）

    请生成一组全面的分析问题，这些问题应涵盖但不限于以下几个方面：
    1. 数据筛选和过滤（如时间范围、批次、产品类型等）
    2. 数据差异性对比（如批次之间、测量阶段之间）
    3. 数据表现趋势（如随时间变化、测量阶段变化）
    4. 数据可视化需求（如需要哪些类型的图表展示）
    5. 关联性和分组分析（如参数与产品类型的关联性）

    请以结构化的方式输出问题，确保每个字段都能引导至少3个数据分析相关问题。
    """    
    # 请以结构化的方式输出问题，确保每个字段都能引导至少3个数据分析相关问题。
    #  
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你是一个半导体专家"},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )
                
    content = response.choices[0].message.content
            
    print(content)
    

    
import json
def save_json(path,obj):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=4)
        
