import discord
from discord.ext import commands


class Help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(title="Help", description=None, color=discord.Color.orange())
        embed.add_field(name="Fun", value="8ball, Ping, Meme, Clone, Sum", inline=False)
        embed.add_field(name="Admin", value="Clear, Kick, Ban, Unban", inline=False)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))
