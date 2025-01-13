import os


import json
def load_json(path):
    with open(path,encoding='utf-8') as f:
        return  json.load(f)

error_count = 0
error_list = []
from tqdm import tqdm
for file in tqdm(os.listdir("data")[:5000]):
    if len(load_json(f'data/{file}')['content']) < 100:
    
        error_list.append(file) 
        error_count += 1
print(error_count)


open("content_error_list.txt",'w').writelines(line + '\n' for line in error_list)