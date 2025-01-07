import pandas as pd



lines = open("./url_2025-0106.txt").readlines()


before_deduplication_count = len(lines)
print(f"before_deduplication_count : {before_deduplication_count}")
deduplication = list(set(lines))
print(f'after_deduplication_count: {len(deduplication)}')

# print(df)
deduplication_file = [item.strip() for item in deduplication if not item.strip().endswith(('.pdf','.docx','.doc'))]
print(f"deduplication(pdf,docx,doc...file):{len((deduplication_file))}")
items = [item.strip() for item in deduplication_file if 'youtube' not in item.strip()]
print(f"deduplication(youtuebe video):{len((items))}")


open('deduplication.url.txt','w').writelines(item + '\n' for item in items)

# data  = pd.read_csv("url_2025-0106.txt",sep=',')

# print(data)