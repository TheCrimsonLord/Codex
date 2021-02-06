import asyncio

import discord
from discord.ext import commands

from main import bot


class Owner(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.is_owner()
    @commands.command(brief="Log out")
    async def die(self, ctx):
        await ctx.send("Bye :(")
        await asyncio.sleep(5)
        await self.bot.logout()

    @commands.is_owner()
    @commands.command(brief="Sends info about bot")
    async def botinfo(self, ctx):
        embed = discord.Embed(title="Bot Information", description=None, color=discord.Color.random())
        embed.add_field(name="Latency", value=f"{round(self.bot.latency * 1000)}ms", inline=False)
        embed.add_field(name="Servers", value="I'm in " + str(len(bot.guilds)) + " servers", inline=False)
        embed.add_field(name="Discord Version", value=discord.__version__, inline=False)
        await ctx.send(embed=embed, content=None)


def setup(bot):
    bot.add_cog(Owner(bot))
