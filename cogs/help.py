import discord
from discord.ext import commands

from main import bot


class Help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="Shows help for a command", aliases=["h"])
    async def help(self, ctx):
        embed = discord.Embed(title="Help", color=discord.Color.orange())
        embed.add_field(name="Fun", value="8Ball, Ping, Meme, Clone, Kill")
        embed.add_field(name="Admin", value="Kick, Ban, Unban, Clear, Set Rules, Perms, Set Prefix")
        embed.set_thumbnail(url=bot.user.avatar_url)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))
