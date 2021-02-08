import asyncio

import discord
from discord.ext import commands

from main import bot


class Owner(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.is_owner()
    @commands.command(brief="Logs out the bot", aliases=["forcequit", "forcestop", "ddos"])
    async def die(self, ctx):
        user = ctx.message.author.display_name
        embed = discord.Embed(title=f"Codex has been forcefully stopped by {user}", color=discord.Color.random())
        for guild in bot.guilds:
            for channel in guild.channels:
                if channel.id == 803109205699461123:
                    await channel.send(embed=embed)
        await asyncio.sleep(1)
        await self.bot.logout()


def setup(bot):
    bot.add_cog(Owner(bot))
