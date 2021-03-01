import datetime
import platform
from typing import Optional

import discord
from discord import Member
from discord.ext import commands

import codex


class Info(commands.Cog):

    def __init__(self, bot: codex.CodexBot):
        self.bot = bot

    @commands.command(brief="Gives info about bot", aliases=["stats"])
    async def botinfo(self, ctx: codex.CodexContext):
        await ctx.embed(title="Bot Information",
                        fields=
                        [("Latency", f"{round(self.bot.latency * 1000)}ms"),
                         ("Uptime", datetime.datetime.now()),
                         ("Servers", f"I'm in {str(len(self.bot.guilds))} servers"),
                         ("Discord Version", discord.__version__),
                         ("Python Version", platform.python_version()),
                         ("GitHub", "Want to see all of the code for the bot, check out the GitHub [here]("
                                    "https://github.com/TheCrimsonLord/Codex)"),
                         ("Support Server", "Need help, join [here](https://discord.gg/g8G7QvPVas)")],
                        thumbnail=self.bot.user.avatar_url,
                        not_inline=[0, 1, 2, 4, 5, 6])

    @commands.command(brief="Shows info on a user", aliases=["uinfo"])
    async def userinfo(self, ctx: codex.CodexContext, user: Optional[Member]):
        user = user or ctx.author
        joined_at = user.joined_at.strftime("%c")
        created_at = user.created_at.strftime("%c")
        r: discord.Role
        hoisted_roles = [r for r in user.roles if r.hoist and r.id != ctx.guild.id]
        normal_roles = [r for r in user.roles if not r.hoist and r.id != ctx.guild.id]
        await ctx.embed(title=f"Info for {user}",
                        fields=
                        [("ID", user.id),
                         ("Joined Server", joined_at),
                         ("Joined Discord", created_at),
                         (f"Hoisted Roles ({len(hoisted_roles)})",
                          ' '.join([r.mention for r in hoisted_roles[:-6:-1]]) if hoisted_roles else 'None'),
                         (f"Normal Roles ({len(normal_roles)})",
                          " ".join([r.mention for r in normal_roles[:-6:-1] if
                                    r.id not in [x.id for x in hoisted_roles]]) if
                          len(normal_roles) > 1 else "None"),
                         ("Top Role", user.roles[-1].mention if len(user.roles) > 1 else "None")],
                        thumbnail=self.bot.user.avatar_url)

    @commands.command(brief="Shows info about a server", aliases=["guildinfo"])
    async def serverinfo(self, ctx: codex.CodexContext):
        await ctx.embed(title=f"Server information for {ctx.guild.name}",
                        fields=
                        [("ID", ctx.guild.id),
                         ("Owner", ctx.guild.owner),
                         ("Region", ctx.guild.region),
                         ("Created at", ctx.guild.created_at.strftime("%c")),
                         ("Members", ctx.guild.member_count),
                         ("Text channels", len(ctx.guild.text_channels)),
                         ("Voice channels", len(ctx.guild.voice_channels)),
                         ("Categories", len(ctx.guild.categories)),
                         ("Roles", len(ctx.guild.roles))],
                        thumbnail=ctx.guild.icon_url)


def setup(bot):
    bot.add_cog(Info(bot))
