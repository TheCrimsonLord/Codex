import discord
from discord.ext import commands


class Help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="Shows help for a command", aliases=["h"])
    async def help(self, ctx):
        embed = discord.Embed(title="Help", color=discord.Color.random())
        fields = [("Fun", "8Ball, Ping, Meme, Clone, Kill", True),
                  ("Admin", "Kick, Ban, Unban, Clear, Set Rules, Perms, Set Prefix, Create Role", True),
                  ("Info", "Botinfo, Serverinfo, Userinfo", True)]
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))
