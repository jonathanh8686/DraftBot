import json
from collections import OrderedDict
from discord.ext import tasks, commands
import asyncio
import discord
import cassiopeia as cass

class History(commands.Cog):

    @commands.command()
    async def leaderboard(self, ctx):
        await ctx.channel.send("Fetching leaderboard...")
        wr = json.loads(open("data/winrates.txt", "r").read())

        sortwr = OrderedDict(sorted(wr.items(), key=lambda x: -(x[1][0]+1)/(sum(x[1])+2)))

        msg = discord.Embed(title=":trophy: Leaderboard :trophy:", color=0xfff81f)
        wrstr = ""
        for p in sortwr:
            wrstr += "**" + str(p) + "**:\t" + "/".join(list(map(str,sortwr[p]))) + "\n"

        msg.add_field(name="Results", value=wrstr)
        await ctx.channel.send("", embed=msg)




    @commands.command(aliases=["winrates"])
    async def winrate(self, ctx):
        await ctx.channel.send("Fetching win-rate data...")
        wr = json.loads(open("data/winrates.txt", "r").read())

        sortwr = OrderedDict(sorted(wr.items(), key=lambda x: -sum(x[1])))

        msg = discord.Embed(title=":trophy: Win Rates :trophy:", color=0xfff81f)
        wrstr = ""
        for p in sortwr:
            wrstr += "**" + str(p) + "**:\t" + "/".join(list(map(str,sortwr[p]))) + "\n"

        msg.add_field(name="Results", value=wrstr)
        await ctx.channel.send("", embed=msg)




def setup(bot):
   bot.add_cog(History(bot))

