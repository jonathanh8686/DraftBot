import discord
import requests
import time
from discord.ext import commands, tasks
import asyncio
import json


conf = json.loads(open("config.json", "r").read())
def spec_api(summonerid):
    url = "https://na1.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/" + summonerid
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://developer.riotgames.com",
        "X-Riot-Token": conf["API_Key"]
    }
    r = requests.get(url, headers=headers)

    return json.loads(r.content)

class Listen(commands.Cog):
    active = False
    players = json.loads(open("data/players.txt", "r").read())


    @commands.command()
    async def check(self, ctx):
        for player in self.players:
            matchdata = (spec_api(self.players[player]))
            if("gameId" not in matchdata):
                print("No game found")
                continue

            if(matchdata["gameType"] != "CUSTOM_GAME"):
                print("Not custom game type")
                continue

            print(str(player) + " found in custom game!")
            summlist = []
            for p in matchdata["participants"]:
                summlist.append(p["summonerName"])
            print("Found summoners:\t" + " ".join(summlist))

            f = open("data/matchplayers.txt", "wr")
            cdict = json.loads(f.read())
            if(matchdata["gameId"] not in cdict):
                print("Writing game data for: " + str(matchdata["gameId"]))
                cdict[matchdata["gameId"]] = summlist
            f.write(json.dumps(cdict))


def setup(bot):
    bot.add_cog(Listen(bot))


