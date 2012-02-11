import json
f = open('sources.json')
print json.load(f)['sources']
