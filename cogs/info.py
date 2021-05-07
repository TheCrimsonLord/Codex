import platform
from datetime import datetime
from typing import Optional, List

import discord
from discord import Member
from discord.ext import commands, tasks

import codex
from libs.conversions import dhm_notation


class Info(commands.Cog):

    def __init__(self, bot: codex.CodexBot):
        self.bot = bot
        self.ping: int = 0
        self.ping_run: List[int] = []
        self.avg_ping: int = 0

    @property
    def description(self):
        return "Info commands"

    @tasks.loop(seconds=2)
    async def resource_loop(self):
        self.ping = round(self.bot.latency * 1000)
        self.ping_run.append(self.ping)
        if len(self.ping_run) > 30 * 60:
            del self.ping_run[0]
        self.avg_ping = round(sum(self.ping_run) / len(self.ping_run))

    @commands.command(brief="Gives info about bot", aliases=["stats"])
    async def botinfo(self, ctx: codex.CodexContext):
        text_channels = 0
        voice_channels = 0
        for channel in self.bot.get_all_channels():
            if isinstance(channel, discord.TextChannel):
                text_channels += 1
            if isinstance(channel, discord.VoiceChannel):
                voice_channels += 1
        await ctx.embed(title="Bot Information", author=f"Codex v1.0.5",
                        fields=
                        [("Ping", f"{round(self.bot.latency * 1000)} ms\n"
                                  f"{self.avg_ping} ms (1h average)"),
                         ("Messages", f"{self.bot.messages}"),
                         ("Commands\nExecuted", f"{self.bot.commands_executed}"),
                         ("Uptime", dhm_notation(datetime.now() - self.bot.start_time)),
                         ("Presence", f"{len(self.bot.guilds)} Guilds\n"
                                      f"{text_channels} Text Channels\n"
                                      f"{voice_channels} Voice Channels\n"
                                      f"{len(self.bot.users)} Users Cached"),

                         ("Discord Version", discord.__version__),
                         ("Python Version", platform.python_version()),
                         ("GitHub", "Want to see all of the code for the bot, check out the GitHub [here]("
                                    "https://github.com/TheCrimsonLord/Codex)"),
                         ("Want me in your own server?", "Invite me [here](http://bit.ly/CodexBot)"),
                         ("Support Server", "Need help, join [here](https://discord.gg/g8G7QvPVas)")],
                        thumbnail=self.bot.user.avatar_url)

    @commands.command(brief="Shows info on a user", aliases=["uinfo"])
    async def userinfo(self, ctx: codex.CodexContext, user: Optional[Member]):
        user = user or ctx.author
        joined_at = user.joined_at.strftime("%c")
        created_at = user.created_at.strftime("%c")
        r: discord.Role
        hoisted_roles = [r for r in user.roles if r.hoist and r.id != ctx.guild.id]
        normal_roles = [r for r in user.roles if not r.hoist and r.id != ctx.guild.id]
        await ctx.embed(author=f"Info for {user}", icon=user.avatar_url,
                        fields=
                        [("ID", user.id),
                         ("Joined Server", joined_at),
                         ("Joined Discord", created_at),
                         (f"Hoisted Roles ({len(hoisted_roles)})",
                          " ".join([r.mention for r in hoisted_roles[:-6:-1]]) if hoisted_roles else "None"),
                         (f"Normal Roles ({len(normal_roles)})",
                          " ".join([r.mention for r in normal_roles[:-6:-1] if
                                    r.id not in [x.id for x in hoisted_roles]]) if
                          len(normal_roles) > 1 else "None"),
                         ("Top Role", user.roles[-1].mention if len(user.roles) > 1 else "None")])

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
                         ("Roles", len(ctx.guild.roles) - 1)],
                        thumbnail=ctx.guild.icon_url)


def setup(bot):
    bot.add_cog(Info(bot))
