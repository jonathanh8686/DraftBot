from discord.ext import tasks, commands
import asyncio
import discord
import cassiopeia as cass

class History(commands.Cog):


    @commands.command()
    async def leaderboard(self, ctx):
        await ctx.channel.send("Getting leaderboard data... This may take a while :alarm_clock:")

        #TODO: this

def setup(bot):
   bot.add_cog(History(bot))
