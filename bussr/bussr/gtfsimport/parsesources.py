import json
f = open('sources.json')
# print json.loads('{ "sources":[{"hi":"0"}] }')

settings_text = open("sources.json", "r").read()
print settings_text
settings = json.loads(settings_text)
print settings
f.close()
