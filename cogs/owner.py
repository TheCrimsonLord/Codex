import asyncio
import discord
from discord.ext import commands

from main import bot


class Owner(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.is_owner()
    @commands.command(brief="Logs out the bot", aliases=["forcequit", "forcestop"])
    async def die(self, ctx):
        user = ctx.message.author.display_name
        embed = discord.Embed(title=f"Codex has been forcefully stopped by {user}", color=discord.Color.random())
        for guild in bot.guilds:
            for channel in guild.channels:
                if channel.id == 803109205699461123:
                    await channel.send(embed=embed)
        await asyncio.sleep(5)
        await self.bot.logout()

    @commands.is_owner()
    @commands.command(brief="Sends info about bot")
    async def botinfo(self, ctx):
        embed = discord.Embed(title="Bot Information", color=discord.Color.random())
        embed.add_field(name="Latency", value=f"{round(self.bot.latency * 1000)}ms", inline=False)
        embed.add_field(name="Servers", value="I'm in " + str(len(bot.guilds)) + " servers", inline=False)
        embed.add_field(name="Discord Version", value=discord.__version__, inline=False)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Owner(bot))
