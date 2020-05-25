import json

match_data = json.loads(open("data/matchdata.txt", "r").read())
player_data = json.loads(open("data/matchplayers.txt", "r").read())


def get_kda():
    kda = {}
    for m_id in match_data:
        match = match_data[m_id]
        pc = player_data[m_id]
        for p in match["participants"]:
            sum_name = pc[p["participantId"] - 1]
            if(sum_name not in kda):
                kda[sum_name] = [0, 0, 0]
            kda[sum_name][0] += p["stats"]["kills"]
            kda[sum_name][1] += p["stats"]["deaths"]
            kda[sum_name][2] += p["stats"]["assists"]
    return kda

def get_stat_per_minute(statName):
    rtn, gamedur  = {}, {}
    for m_id in match_data:
        match = match_data[m_id]
        pc = player_data[m_id]

        for p in match["participants"]:
            sum_name = pc[p["participantId"] - 1]
            if(sum_name not in rtn):
                rtn[sum_name] = 0

            if(sum_name not in gamedur):
                gamedur[sum_name] = 0
            gamedur[sum_name] += match["gameDuration"]/60
            rtn[sum_name] += p["stats"][statName]

    for p in rtn:
        rtn[p] /= gamedur[p]
    return rtn

def get_stat_per_game(statName):
    rtn, gamecount  = {}, {}
    for m_id in match_data:
        match = match_data[m_id]
        pc = player_data[m_id]

        for p in match["participants"]:
            sum_name = pc[p["participantId"] - 1]
            if(sum_name not in rtn):
                rtn[sum_name] = 0

            if(sum_name not in gamecount):
                gamecount[sum_name] = 0
            gamecount[sum_name] += 1
            rtn[sum_name] += p["stats"][statName]

    for p in rtn:
        rtn[p] /= gamecount[p]
    return rtn


def get_stat(statName):
    rtn = {}
    for m_id in match_data:
        match = match_data[m_id]
        pc = player_data[m_id]

        for p in match["participants"]:
            sum_name = pc[p["participantId"] - 1]
            if(sum_name not in rtn):
                rtn[sum_name] = 0

            rtn[sum_name] += p["stats"][statName]

    return rtn

def stat_string_per_minute(statName):
    s = sorted(get_stat_per_minute(statName).items(), key=lambda x:-x[1])
    rtn = ""
    for p in s:
        rtn += ("**" + p[0] + "**:\t" + str(p[1])) + "\n"
    return rtn

def stat_string_per_game(statName):
    s = sorted(get_stat_per_game(statName).items(), key=lambda x:-x[1])
    rtn = ""
    for p in s:
        rtn += ("**" + p[0] + "**:\t" + str(p[1])) + "\n"
    return rtn

def stat_string(statName):
    s = sorted(get_stat(statName).items(), key=lambda x:-x[1])
    rtn = ""
    for p in s:
        rtn += ("**" + p[0] + "**:\t" + str(p[1])) + "\n"
    return rtn

print(stat_string("quadraKills"))




## get kda string
#s = sorted(get_kda().items(), key=lambda x:-(x[1][0] + x[1][2])/x[1][1])
#for p in s:
#    score = (p[1][0] + p[1][2]) / p[1][1]
#    print(str(p) + "\t" + str(score))
##get cspm string
#s = sorted(get_stat_per_minute("totalMinionsKilled").items(), key=lambda x:-x[1])
#for p in s:
#    print("**" + p[0] + "**:\t" + str(p[1]))

##get dpm string
#s = sorted(get_stat_per_minute("totalDamageDealt").items(), key=lambda x:-x[1])
#for p in s:
#    print("**" + p[0] + "**:\t" + str(p[1]))


##get visionscore string
#s = sorted(get_stat_per_game("visionScore").items(), key=lambda x:-x[1])
#for p in s:
#    print("**" + p[0] + "**:\t" + str(p[1]))

##get damagetaken pm string
#s = sorted(get_stat_per_minute("totalDamageTaken").items(), key=lambda x:-x[1])
#for p in s:
#    print("**" + p[0] + "**:\t" + str(p[1]))

##get objective damage string













