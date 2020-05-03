import json
import requests

conf = json.loads(open("config.json", "r").read())
match_ids = [x.strip()  for x in open("data/matches.txt", "r").readlines()]

def save_json(match_ids, outpath = "data/matchdata.txt"):
    all_dict = {}
    url = "https://na1.api.riotgames.com/lol/match/v4/matches/"
    hdrs= {"X-Riot-Token": conf["API_Key"]}
    for m in match_ids:
        print(url + str(m))
        all_dict[m] = str(requests.get(url + str(m), headers=hdrs).content)

    open(outpath, "w+").write(json.dumps(all_dict))

def get_winloss(match_dict):
    res = {}
    for m in match_dict:
        s = match_dict[m][2:-1]
        mdic = json.loads(s)
        for p in mdic["participantIdentities"]:
            print(p)
            print(p.player.summonerName)



match_str = open("data/matchdata.txt", "r").read()
get_winloss(json.loads(match_str))

