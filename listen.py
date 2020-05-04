import discord
from discord.ext import commands, tasks
import json

active = False

players = json.loads(open("data/players.txt", "r").read())
print(players.values())


@tasks.loop(seconds=5.0)
async def check_spectator():
    print("test")

check_spectator().start()

def start_listening():
    pass

def stop_listening():
    pass




