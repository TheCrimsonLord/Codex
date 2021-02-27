import platform
from typing import Optional

import discord
from discord import Member, message
from discord.ext import commands
import datetime

from main import bot


class Info(commands.Cog):

    def __init__(self, _bot):
        self.bot = bot

    @commands.command(brief="Gives info about bot", aliases=["stats"])
    async def botinfo(self, ctx):
        embed = discord.Embed(title="Bot Information", color=discord.Color.random())
        fields = [("Latency", f"{round(self.bot.latency * 1000)}ms", False),
                  ("Uptime", datetime, False),
                  ("Servers", f"I'm in {str(len(bot.guilds))} servers", False),
                  ("Discord Version", discord.__version__, False),
                  ("Python Version", platform.python_version(), False),
                  ("GitHub", "Want to see all of the code for the bot, check out the GitHub [here]("
                             "https://github.com/TheCrimsonLord/Codex)", False),
                  ("Support Server", "Need help, join [here](https://discord.gg/g8G7QvPVas)", False)]
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
        await ctx.send(embed=embed)

    @commands.command(brief="Shows info on a user", aliases=["uinfo"])
    async def userinfo(self, ctx, user: Optional[Member]):
        user = user or ctx.author
        joined_at = user.joined_at.strftime("%c")
        created_at = user.created_at.strftime("%c")
        r: discord.Role
        hoisted_roles = [r for r in user.roles if r.hoist and r.id != ctx.guild.id]
        normal_roles = [r for r in user.roles if not r.hoist and r.id != ctx.guild.id]
        embed = discord.Embed(title=f"Info for {user}", color=discord.Color.random())
        fields = [("ID", user.id, True),
                  ("Joined Server", joined_at, True),
                  ("Joined Discord", created_at, True),
                  (f"Hoisted Roles ({len(hoisted_roles)})",
                   ' '.join([r.mention for r in hoisted_roles[:-6:-1]]) if hoisted_roles else 'None', True),
                  (f"Normal Roles ({len(normal_roles)})",
                   " ".join([r.mention for r in normal_roles[:-6:-1] if r.id not in [x.id for x in hoisted_roles]]) if
                   len(normal_roles) > 1 else "None", True),
                  ("Top Role", user.roles[-1].mention if len(user.roles) > 1 else "None", True)]
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
        embed.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(aliases=["guildinfo"])
    async def serverinfo(self, ctx):
        embed = discord.Embed(title=f"Server information for {ctx.guild.name}", color=discord.Color.random())
        embed.set_thumbnail(url=ctx.guild.icon_url)
        fields = [("ID", ctx.guild.id, True),
                  ("Owner", ctx.guild.owner, True),
                  ("Region", ctx.guild.region, True),
                  ("Created at", ctx.guild.created_at.strftime("%c"), True),
                  ("Members", ctx.guild.member_count, True),
                  ("Text channels", len(ctx.guild.text_channels), True),
                  ("Voice channels", len(ctx.guild.voice_channels), True),
                  ("Categories", len(ctx.guild.categories), True),
                  ("Roles", len(ctx.guild.roles), True),
                  ("\u200b", "\u200b", True)]
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
        await ctx.send(embed=embed)


def setup(_bot):
    bot.add_cog(Info(bot))
