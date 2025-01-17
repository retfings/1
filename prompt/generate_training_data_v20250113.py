import json
import pandas as pd
from pathlib import Path
import asyncio
from openai import AsyncOpenAI
import re
from tqdm import tqdm

class TrainingDataGenerator:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent.parent
        self.client = AsyncOpenAI(
            api_key="sk-c765e87a50df47cfb82b0c16c6da0066", 
            base_url="https://api.deepseek.com"
        )
        
    async def generate_questions(self, row, num_questions=5):
        """使用大模型生成问题"""
        conditions = row['查询条件'].split('、') if pd.notna(row['查询条件']) else []
        keywords = row['关键字'].split('、') if pd.notna(row['关键字']) else []
        original_questions = row['问题'].split('\n') if pd.notna(row['问题']) else []
        
        prompt = f"""
请根据以下信息生成{num_questions}个查询问题：

数据类型: {row['Data Type']}
可用的查询条件: {', '.join(conditions)}
相关关键词: {', '.join(keywords)}
原始问题示例:
{chr(10).join(original_questions)}

要求：
1. 每个问题必须包含至少一个查询条件
2. 必须包含时间范围或lot_no作为条件,二者不同时存在
3. 必须组合多个查询条件，但是组合要根据数据类型和查询条件来
4. 问题要自然且符合业务场景
5. 参考原始问题的风格
6. 确保使用的条件都在给定的查询条件列表中

请直接返回JSON数组格式，每个元素包含一个问题字符串。不要包含其他说明文字。
"""
        # print(prompt)
        
        try:
            response = await self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that generates natural business questions in Chinese. Always respond with valid JSON array."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0
            )
            
            content = response.choices[0].message.content
            questions = json.loads(content)
            

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
        csv_path = "data.csv"
        df = pd.read_csv(csv_path, encoding='utf-8')
        
        training_data = []
        
        # 并发处理所有行
        tasks = [self.process_row(row) for _, row in df.iterrows()]
        # tasks = tasks[0]
        results = await asyncio.gather(tasks)
        
        # 合并结果
        for result in results:
            training_data.extend(result)
        
        from datetime import datetime
        current_date = datetime.now()
        timestamp = int(current_date.timestamp())
        version_string = current_date.strftime("v%Y%m%d")
        version_string = f"{version_string}_{timestamp}"
        # 保存训练数据
        output_path = f"training_data_{version_string}.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(training_data, f, ensure_ascii=False, indent=2)
        
        print(f"\nTotal generated examples: {len(training_data)}")
        print(f"Training data saved to: {output_path}")
        
        # 打印一些示例
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