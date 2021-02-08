import sys

import discord
from discord.ext import commands

from main import bot


class Utils(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="Sends info about bot", aliases=["stats"])
    async def botinfo(self, ctx):
        pyver = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        embed = discord.Embed(title="Bot Information", color=discord.Color.random())
        embed.add_field(name="Latency", value=f"{round(self.bot.latency * 1000)}ms", inline=False)
        embed.add_field(name="Servers", value="I'm in " + str(len(bot.guilds)) + " servers", inline=False)
        embed.add_field(name="Discord Version", value=discord.__version__, inline=False)
        embed.add_field(name="Python Version", value=pyver, inline=False)
        await ctx.send(embed=embed)

    @commands.command(brief="Shows info on a user", aliases=["uinfo"])
    async def userinfo(self, ctx, user: discord.User):
        if not user:
            user = ctx.author
        joined_at = user.joined_at.strftime("%c")
        created_at = user.created_at.strftime("%c")
        r: discord.Role
        hoisted_roles = [r for r in user.roles if r.hoist and r.id != ctx.guild.id]
        normal_roles = [r for r in user.roles if not r.hoist and r.id != ctx.guild.id]
        embed = discord.Embed(title=f"Info for {user}")
        embed.add_field(name="ID", value=user.id)
        embed.add_field(name="Joined Server", value=joined_at)
        embed.add_field(name="Joined Discord", value=created_at)
        embed.add_field(name=f"Hoisted Roles ({len(hoisted_roles)})",
                        value=' '.join([r.mention for r in hoisted_roles[:-6:-1]]) if hoisted_roles else 'None')
        embed.add_field(name=f"Normal Roles ({len(normal_roles)})",
                        value=" ".join([r.mention for r in normal_roles[:-6:-1] if
                                        r.id not in [x.id for x in hoisted_roles]]) if len(
                            normal_roles) > 1 else "None")
        embed.add_field(name="Top Role", value=user.roles[-1].mention if len(user.roles) > 1 else "None")
        embed.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Utils(bot))
