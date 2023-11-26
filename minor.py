import json

j = json.load(open("algolia.json"))

for k, v in j['results'][0].items():
    if k == 'hits':
        json.dump(v, open("companies.json", "w"))
    
    if k == 'facets':
        json.dump(v, open("stats.json", "w"))