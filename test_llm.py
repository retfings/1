def llam():

  from ollama import chat
  from pydantic import BaseModel

  class Country(BaseModel):
    name: str
    capital: str
    languages: list[str]

  response = chat(
    messages=[
      {
        'role': 'user',
        'content': '你好',
      }
    ],
    model='qwen2.5',
    format=Country.model_json_schema(),
  )

  country = Country.model_validate_json(response.message.content)
  print(country)
  
  
  
  
def deepseekv3():
  
  pass
from openai import OpenAI

client = OpenAI(api_key="sk-c765e87a50df47cfb82b0c16c6da0066", base_url="https://api.deepseek.com")

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "user", "content": "Hello"},
    ],
    stream=False
)

print(response)


