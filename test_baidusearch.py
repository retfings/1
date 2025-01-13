from baidusearch.baidusearch import search

results = search('半导体',num_results=3)  # returns 10 or less results

for r in results:
    print(r['url'])
    print()
# print(results)

import requests
data = requests.get(r['url'])

print(data.content)