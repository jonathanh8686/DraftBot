import json
import requests

conf = json.loads(open("config.json", "r").read())
matchplayer = json.loads(open("data/matchplayers.txt", "r").read())


def save_json(match_ids, outpath = "data/matchdata.txt"):
    all_dict = {}
    url = "https://na1.api.riotgames.com/lol/match/v4/matches/"
    hdrs= {"X-Riot-Token": conf["API_Key"]}
    for m in match_ids:
        print("Requesting:\t" + url + str(m))
        all_dict[m] = json.loads(str(requests.get(url + str(m), headers=hdrs).content)[2:-1])
    open(outpath, "w+").write(json.dumps(all_dict))

def get_winloss(match_dict):
    wrdict = {}
    for match in match_dict:
        cm = match_dict[match]

        teamwinId = -1
        if(cm["teams"][0]["teamId"] == 100): # lol maybe make this better one day
            if(cm["teams"][0]["win"] == "Win"):
                teamwinId = 100
            else:
                teamwinId = 200

        for p in cm["participants"]:
            pid = p["participantId"] - 1
            cnme = matchplayer[match][pid]

            if(cnme not in wrdict):
                wrdict[cnme] = [0, 0]

            adjwinid = (teamwinId//100) - 1

            if(pid//5 == adjwinid): # lol what
                wrdict[cnme][0] += 1
            else:
                wrdict[cnme][1] += 1
    return wrdict


save_json(matchplayer.keys())
match_str = open("data/matchdata.txt", "r").read()
open("data/winrates.txt", "w").write(json.dumps(get_winloss(json.loads(match_str))))




