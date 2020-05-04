#!/usr/bin/env python3

from discord.ext import commands, tasks
import json
import discord
from datetime import datetime
from time import gmtime, strftime
from threading import Timer

bot = commands.Bot(command_prefix="-")
cogs = ["history"]

CHAMPIONS = [x.strip().lower() for x in open("data/champions.txt", "r").read().split(",")]

blue_cap, red_cap = None, None

blue_bans, blue_picks = [], []
red_bans, red_picks = [], []

indraft = False
cmessage = None

PICK_STATE = ["BB", "RB", "BB", "RB", "BB", "RB", "BP", "RP", "RP", "BP", "BP", "RP", "RB", "BB", "RB", "BB", "RP", "BP", "BP", "RP"]
curr_state = prev_state = -1


#TODO: add some fuzzy string matching for champion selection?
#TODO: fix this global shit

@tasks.loop(seconds=1)
async def update_timer():
    global cmessage

    if(cmessage == None):
        update_timer.stop()
        return

    await bot.wait_until_ready()

    ct = int(cmessage.content.split("(")[1].split(")")[0])
    nct = ct - 1

    await cmessage.edit(content=cmessage.content.split("(")[0] + "(" + str(nct) + ")")

    if(nct == 0):
        # maybe can force select a random champion if needed
        update_timer.stop()
        return



async def play_state(channel):
    global curr_state, prev_state
    global indraft
    global blue_picks, blue_bans
    global red_picks, red_bans
    global blue_cap, red_cap
    global cmessage

    print(red_picks)
    print(blue_picks)

    if(curr_state == len(PICK_STATE)):
        await channel.send("Draft over! :checkered_flag:")

        blueteam = discord.Embed(title=":blue_circle: Blue Team :blue_circle:", color=0x0000ff)
        blueteam.add_field(name="Picks:", value="\n".join([x.upper() for x in blue_picks]))
        await channel.send("", embed=blueteam)

        redteam = discord.Embed(title=":red_circle: Red Team :red_circle:", color=0xff0000)
        redteam.add_field(name="Picks:", value="\n".join([x.upper() for x in red_picks]))
        await channel.send("", embed=redteam)

        blue_cap = None
        red_cap = None
        blue_bans = []
        blue_picks = []
        red_bans = []
        red_picks = []

        indraft = False
        curr_state = -1
        prev_state = -1

        print(blue_picks)
        print(red_picks)

        return

    state = PICK_STATE[curr_state]
    msg = ""
    if(state[0] == "B"):
        msg += ":blue_circle:" + blue_cap.mention + ": "
    elif(state[0] == "R"):
        msg += ":red_circle:" + red_cap.mention + ": "

    if(state[1] == "B"):
        msg += "BANNING (30)"
    elif(state[1] == "P"):
        msg += "PICKING (30)"

    curr_state += 1
    cmessage = await channel.send(msg)
    try:
        update_timer.start()
    except:
        pass # asdlfkjasdflkjasdflkjasdflkajlefkajwlfjbawlgkwhr fix never


@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))

@bot.command()
async def ping(ctx):
    await ctx.send("pong!")


@bot.command()
async def blue(ctx):
    global blue_cap
    global red_cap
    if(blue_cap != None):
        await ctx.send(":x: Already have a blue team captain! :blue_circle:")
        return
    if(ctx.message.author == red_cap):
        await ctx.send(":x: You are already the red team captain! :red_circle:")
        return

    blue_cap = ctx.message.author

    await ctx.send(":blue_circle: Blue team captain initalized! :white_check_mark:")

@bot.command()
async def red(ctx):
    global blue_cap
    global red_cap
    if(red_cap != None):
        await ctx.send(":x: Already have a red team captain! :red_circle:")
        return
    if(ctx.message.author == blue_cap):
        await ctx.send(":x: You are already the blue team captain! :blue_circle:")
        return

    red_cap = ctx.message.author

    await ctx.send(":red_circle: Red team captain initalized! :white_check_mark:")

@bot.command()
async def start(ctx):
    global indraft
    global curr_state
    if(red_cap == None):
        await ctx.send(":X: Missing red team captain! :x:")
        return
    if(blue_cap == None):
        await ctx.send(":x: Missing blue team captain! :x:")
        return

    if(ctx.message.author == red_cap or ctx.message.author == blue_cap):
        indraft = True
        curr_state = 0
        await ctx.send(":robot: Starting draft... :robot:")
        await play_state(ctx.channel)


@bot.command()
async def reset(ctx):
    global blue_cap, red_cap, blue_picks, blue_bans, red_picks, red_bans
    global indraft
    if(ctx.author.id == 141642956753862656):
        await ctx.send("Resetting all variables. :checkered_flag:")
        blue_cap = None
        red_cap = None
        blue_picks = []
        blue_bans = []
        red_picks = []
        red_bans = []
        curr_state = -1
        prev_state = -1
        indraft = False


@bot.event
async def on_message(message):
    global indraft
    global prev_state
    global curr_state
    global red_picks, blue_picks, red_bans, blue_bans

    if message.author == bot.user:
        return

    if(message.channel.id != 704551677297950730): # prod
    #if(message.channel.id != 296893697113456640): # bot testing
        return

    print(strftime("%Y-%m-%d %H:%M:%S", gmtime()) + "\t" + str(message.author) + ":\t" + message.content) # record the messages sent

    await bot.process_commands(message)

    if(message.content == "-start"):
        return

    if(indraft == True):
        state = PICK_STATE[curr_state - 1]
        print(state)

        if(state[0] == "B" and message.author != blue_cap):
            await message.delete()
            return

        if(state[0] == "R" and message.author != red_cap):
            await message.delete()
            return


        if(curr_state == prev_state):
            await message.channel.send("Slow down! :stop_sign:")
            return
        prev_state = curr_state

        if(state[0] == "B" and message.author == blue_cap):
            if(message.content.lower() in CHAMPIONS):
                if(state[1] == "B"):
                    if(message.content.lower() in blue_bans or message.content.lower() in red_bans):
                        await message.channel.send(message.content.upper() + " has already been banned! :x:")
                        prev_state = -1
                        return

                    if(message.content.lower() in blue_picks or message.content.lower() in red_picks):
                        await message.channel.send(message.content.upper() + " has already been picked! :x:")
                        prev_state = -1
                        return

                    await message.channel.send("**" + message.content.upper() + "** added to blue team bans!")
                    blue_bans.append(message.content.lower())
                    await play_state(message.channel)
                elif(state[1] == "P"):
                    if(message.content.lower() in blue_bans or message.content.lower() in red_bans):
                        await message.channel.send(message.content.upper() + " is banned! :x:")
                        prev_state = -1
                        return

                    if(message.content.lower() in blue_picks or message.content.lower() in red_picks):
                        await message.channel.send(message.content.upper() + " has already been picked! :x:")
                        prev_state = -1
                        return

                    await message.channel.send("**" + message.content.upper() + "** added to blue team picks!")
                    blue_picks.append(message.content.lower())
                    await play_state(message.channel)
            else:
                await message.channel.send(":x: Champion not found. :x:")
                prev_state = -1

        elif(state[0] == "R" and message.author == red_cap):
            if(message.content.lower() in CHAMPIONS):
                if(state[1] == "B"):
                    if(message.content.lower() in blue_bans or message.content.lower() in red_bans):
                        await message.channel.send(message.content.upper() + " has already been banned! :x:")
                        prev_state = -1
                        return

                    if(message.content.lower() in blue_picks or message.content.lower() in red_picks):
                        await message.channel.send(message.content.upper() + " has already been picked! :x:")
                        prev_state = -1
                        return

                    await message.channel.send("**" + message.content.upper() + "** added to red team bans!")
                    red_bans.append(message.content.lower())
                    await play_state(message.channel)
                elif(state[1] == "P"):
                    if(message.content.lower() in blue_bans or message.content.lower() in red_bans):
                        await message.channel.send(message.content.upper() + " is banned! :x:")
                        prev_state = -1
                        return

                    if(message.content.lower() in blue_picks or message.content.lower() in red_picks):
                        await message.channel.send(message.content.upper() + " has already been picked! :x:")
                        prev_state = -1
                        return

                    await message.channel.send("**" + message.content.upper() + "** added to red team picks!")
                    red_picks.append(message.content.lower())
                    await play_state(message.channel)
            else:
                await message.channel.send(":x: Champion not found. :x:")
                prev_state = -1



configData = json.loads(open("config.json", "r").read())

for c in cogs:
    bot.load_extension(c)
bot.run(configData["bot_token"])




