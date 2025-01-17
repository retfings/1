import json
import pandas as pd
from pathlib import Path
import asyncio
from openai import AsyncOpenAI
import re
from tqdm import tqdm

class TrainingDataGenerator:
    def __init__(self):
        self.project_root = '.'
        self.client = AsyncOpenAI(
            api_key="sk-c765e87a50df47cfb82b0c16c6da0066", 
            base_url="https://api.deepseek.com"
        )
        
    async def generate_questions(self, row, num_questions=5):
        """使用大模型生成问题"""
        conditions = row['查询条件'].split('、') if pd.notna(row['查询条件']) else []
        keywords = row['关键字'].split('、') if pd.notna(row['关键字']) else []
        original_questions = row['问题'].split('\n') if pd.notna(row['问题']) else []
        
        print(keywords)
        extracted_data = {}

        for item in conditions:
            match = re.match(r'(\w+)(?:\(([^)]+)\))?', item)
            if match:
                key = match.group(1)
                value = match.group(2)
                if value:  # Only include keys with values
                    extracted_data[key] = value
        
        # print(extracted_data)
        
        table_name = row['数据表名']  
        keyword_columns = row['查询条件']  
        
        # 相关关键词: {', '.join(keywords)}
        # 数据类型: {row['Data Type']}
        # 原始问题示例: {chr(10).join(original_questions)}
        prompt_v4 = f"""
- 角色：你将模拟人针对特定的查询字典(key为查询字段，value字段可选值)提出{num_questions}个，请结合业务场景（半导体行业,良率分析）提问。
提问时请考虑问题的多样性，一个问题的不同问法。
- 背景：要完成数据合成任务，模拟人工进行提问。问题应该命中1~3个查询字典里面的key和values。
- 任务：根据查询字典里面的key和values，提出一些问题。如果问题里面包含 lot_no，lot_id ，则使用规则3。
- 问题规则：
1. 在xx_time到xx_time,xx_key为xx_values并且xx_key为xx_values的相关数据。其中xx都为<查询字典>里面的数据。
2. 查询近一天|近一周|近一个月|从%Y-%m-%d到%Y-%m-%d，xx_key为xx_values并且xx_key为xx_values的相关数据。
3. 查询xx_key为xx_values并且xx_key为xx_values的相关数据
- 查询字典：{conditions} 
- 关键词: {', '.join(keywords)}
- 数据库表名：{table_name}
- 输出：
* 严格按照json形式输出
* 每个问题一定要符合问题规则
* 返回 ["question1","question2","question3"......]
* 生成问题时应该注重问题的逻辑性，要避免表达不合常理的情况
"""
        prompt_v3 = f"""
- 角色：你将模拟人针对特定的查询字典(key为查询字段，value字段可选值)提出{num_questions}个，请结合业务场景（半导体行业,良率分析）提问。
提问时请考虑问题的多样性，一个问题的不同问法。
- 背景：要完成数据合成任务，模拟人工进行提问。问题应该命中1~3个查询字典里面的key和values。
- 任务：根据查询字典里面的key和values，提出一些问题。
- 问题规则：
1. 在xx_time到xx_time,xx_key为xx_values并且xx_key为xx_values,xx_key的values。其中xx都为<查询字典>里面的数据。<查询字典>和<关键词>如下：
- 查询字典：{conditions} 
- 关键词: {', '.join(keywords)}
- 数据库表名：{table_name}
- 输出：
* 严格按照json形式输出
* 每个问题一定要符合问题规则
* 返回 ["question1","question2","question3"......]
* 生成问题时应该注重问题的逻辑性，要避免表达不合常理的情况
"""
        
        prompt_v2 = f"""
- 角色：你将模拟人针对特定的查询字典(key为查询字段，value字段可选值)提出{num_questions}个，请结合业务场景（半导体行业,良率分析）提问。
提问时请考虑问题的多样性，一个问题的不同问法。
- 背景：要完成数据合成任务，模拟人工进行提问。问题应该命中1~3个查询字典里面的key和values。
- 任务：根据查询字典里面的key和values，提出一些问题。
- 问题规则：
1. 在xx_time到xx_time,xx_key为xx_values并且xx_key为xx_values的<关键词>是什么。其中xx都为<查询字典>里面的数据。<查询字典>和<关键词>如下：
2. 如果存在原始问题，请参考原始问题，并把里面的xx_key，指定xx_values
- 查询字典：{conditions} 
- 关键词: {', '.join(keywords)}
- 数据库表名：{table_name}
- 原始问题示例: {chr(10).join(original_questions)}
- 输出：
* 严格按照json形式输出
* 每个问题一定要符合问题规则
* 返回 ["question1","question2","question3"......]
* 生成问题时应该注重问题的逻辑性，要避免表达不合常理的情况
"""
        prompt_v1 = f"""
- 角色：你将模拟人针对特定的查询字典(key为查询字段，value字段可选值)提出{num_questions}个，请结合业务场景（半导体行业,良率分析）提问。
提问时请考虑问题的多样性，通一个问题的不同问法。
- 背景：要完成数据合成任务，模拟人工进行提问。问题应该命中1~3个查询字典里面的key和values。
- 任务：根据查询字典里面的key和values，提出一些问题。问题规则为在xx_time,xx_key为xx_values的相关数据。其中xx都为查询字典里面的数据。
- 查询字典：{conditions} 
- 数据库表名：{table_name}
- 原始问题示例: {chr(10).join(original_questions)}
- 相关关键词: {', '.join(keywords)}
- 输出：
1. 严格按照json形式输出
2. 返回 ["question1","question2","question3"......]
3. ** 如果查询字段没有实际值，即该字段没有()，则不生成该字段的问题 **
4. 生成问题时应该注重问题的逻辑性，要避免表达不合常理的情况
- 应该要避免的表达问题
1. measure_stage阶段(不合理)，paramter_name的表现如何(不合理)，measure_stage为xxx(正确,xxx替换为具体值)
2. paramter_name在measure_step_seq中的变化趋势(错误)
3. 产品ID为Y086D在**测量阶段的表现如何**？(不合理)，可以问 是否指产品的良率？数据偏差？
4. 批次类型为R的批次A29T216在图 表类型NK上的表现如何(不合理)，应该指明具体那种图表（sitemap叠图）
5. 在测量阶段的具体表现(不合理)，应该指明是那种表现
6. 产品ID为Y086D的晶圆在测量阶段seq中的参数变化趋势是怎样的？(不合理)。建议：参数”没有具体指代某个参数，要指定具体参数。
7. 批次A29T216在测量阶段的具体参数表现如何？(不合理) 要指明具体哪个参数表现
"""
        # 5. 参考原始问题的风格
        prompt = f"""
根据以下查询条件生成{num_questions}个自然且符合业务场景的查询问题：
查询条件: {', '.join(conditions)}
返回json格式: ["question1","question2",...] 
要求：
- 每个问题至少包含一个或多个查询条件。
- 
- 必须包含时间范围或lot_no作为条件，二者不同时出现。
- 自动根据数据类型和查询条件智能组合，减少人工干预。
- 问题应覆盖各类查询场景，确保条件多样化且完整使用。
- 每个字段应能衍生出多个有分析价值的查询问题。
- 直接返回JSON数组格式，每个元素为一个问题字符串，且不包含其他说明文字。
"""

        try:

            response = await self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that generates natural business questions in Chinese. Always respond with valid JSON array."},
                    {"role": "user", "content": prompt_v4}
                ],
                temperature=0
            )

            # print(prompt)
            content = response.choices[0].message.content
            try:
                questions = json.loads(content.replace("```json","").replace("```",""))
                print(questions)
            except:
                print("json load faild")
            return questions
            
        except Exception as e:
            print(f"Error generating questions: {e}")
            return []

    async def process_row(self, row):
        """处理单行数据"""
        if not pd.notna(row['Data Type']):
            return []
            
        base_info = {
            "data_type": row['Data Type'],
            "loader_level": row['Loader Level'],
            "table_name": row['数据表名']
        }
        
        training_data = []
        
        # 1. 添加原始问题
        if pd.notna(row['问题']):
            questions = row['问题'].split('\n')
            for question in questions:
                question = re.sub(r'^\d+\.\s*', '', question).strip()
                if question:
                    training_data.append({
                        "text": question,
                        **base_info,
                        "source": "original"
                    })
        
        # 2. 使用大模型生成新问题
        generated_questions = await self.generate_questions(row)
        for question in generated_questions:

            training_data.append({
                "text": question,
                **base_info,
                "source": "generated"
            })
        
        return training_data

    async def generate_training_data(self):
        """生成训练数据"""
        # 加载原始CSV数据
        csv_path = "带字段名_20250114v1.csv"
        df = pd.read_csv(csv_path, encoding='utf-8')
        
        training_data = []
        
        # 并发处理所有行
        tasks = [self.process_row(row) for _, row in df.head(2).iterrows()]
        results = await asyncio.gather(*tasks)
        
        # 合并结果
        for result in results:
            training_data.extend(result)
        
        
        
        def get_version() -> str:
            from datetime import datetime
            current_date = datetime.now()
            timestamp = int(current_date.timestamp())
            version_string = current_date.strftime("v%Y%m%d")
            return f"{version_string}_{timestamp}"
        # 保存训练数据
        output_path =  f"training_data_{get_version()}.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(training_data, f, ensure_ascii=False, indent=2)
        
        # print(f"\nTotal generated examples: {len(training_data)}")
        # print(f"Training data saved to: {output_path}")
        
        # # 打印一些示例
        # print("\nExample generated data:")
        # for example in training_data[:5]:
        #     print(f"\nText: {example['text']}")
        #     print(f"Data Type: {example['data_type']}")
        #     print(f"Loader Level: {example['loader_level']}")
        #     print(f"Table: {example['table_name']}")
        #     print(f"Source: {example['source']}")
        
        return training_data

async def main():
    generator = TrainingDataGenerator()
    await generator.generate_training_data()

if __name__ == "__main__":
    asyncio.run(main()) 
    # import pandas as pd
    # name = '快捷查询维度说明_processed_20250113_from_tianyi'
    # pd.read_excel(f'{name}.xlsx').to_csv(f'{name}.csv',index=None)