import json


d = json.loads( open("data/matchplayers.txt", "r").read())

print(len(d))
