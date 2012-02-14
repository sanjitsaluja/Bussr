import json
f = open('sources.json')
print json.loads('{ "sources":[{"hi":"0"},] }')
f.close()
