#!/usr/bin/env python3

from discord.ext import commands
import json
import discord
from datetime import datetime
from time import gmtime, strftime
from threading import Timer

bot = commands.Bot(command_prefix="-")

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.command()
async def ping(ctx):
    await ctx.send("pong!")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if(message.channel.id != 287438361528893442):
        return

    print(strftime("%Y-%m-%d %H:%M:%S", gmtime()) + "\t" + str(message.author) + ":\t" + message.content) # record the messages sent
    await bot.process_commands(message)

configData = json.loads(open("config.json", "r").read())

bot.run(configData["bot_token"])
