import datetime as dt
import json
import typing
from typing import Optional

import discord
from discord.ext import commands

import codex


class Admin(commands.Cog):

    def __init__(self, bot: codex.CodexBot):
        self.bot = bot

    @property
    def description(self):
        return "Admin module"

    @commands.command(brief="Clears messages", aliases=["purge"])
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def clear(self, ctx: codex.CodexContext, amount: int = 5):
        stop_at = dt.datetime.now() - dt.timedelta(days=14)
        messages_list = []
        async for message in ctx.channel.history(limit=amount + 1):
            if message.created_at < stop_at:
                break
            messages_list.append(message)
            if len(messages_list) > 90:
                await ctx.channel.delete_messages(messages_list)
                messages_list = []
        await ctx.channel.delete_messages(messages_list)

    @commands.command(brief="Kicks member")
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def kick(self, ctx: codex.CodexContext, member: discord.Member, *, reason=None):
        await member.kick(reason=f"{ctx.author} | {reason}")
        await ctx.embed(title=f"{ctx.author} kicked {member} for {reason}")

    @commands.command(brief="Bans members", aliases=["permkick"])
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def ban(self, ctx: codex.CodexContext, member: discord.Member, *, reason=None):
        await member.ban(reason=f"{ctx.author} | {reason}")
        await ctx.embed(title=f"{ctx.author} banned {member} for {reason}")

    @commands.command(brief="Unbans members")
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def unban(self, ctx: codex.CodexContext, *, member: typing.Union[int, str]):
        banned_users = await ctx.guild.bans()
        for ban_entry in banned_users:
            if (isinstance(member, int) and ban_entry.user.id == member) or \
                    (isinstance(member, str) and member in str(ban_entry.user)):
                await ctx.guild.unban(ban_entry.user, reason=str(ctx.author))
                return await ctx.embed(title=f"{ctx.author} unbanned {ban_entry.user}")

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def setrules(self, ctx: codex.CodexContext, *, inp: str):
        amount: int = 1
        stop_at = dt.datetime.now() - dt.timedelta(days=14)
        messages_list = []
        async for message in ctx.channel.history(limit=amount):
            if message.created_at < stop_at:
                break
            messages_list.append(message)
            if len(messages_list) > 90:
                await ctx.channel.delete_messages(messages_list)
                messages_list = []
        await ctx.channel.delete_messages(messages_list)
        await ctx.embed(title="Rules", description=inp)

    @commands.command(brief="Changes the command prefix", aliases=["cp"])
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def changeprefix(self, ctx: codex.CodexContext, prefix):
        with open("prefixes.json", "r") as f:
            prefixes = json.load(f)
        prefixes[str(ctx.guild.id)] = prefix
        with open("prefixes.json", "w") as f:
            json.dump(prefixes, f, indent=4)
        await ctx.embed(title="Prefix has successfully been changed", description=f"You can now use {prefix} to "
                                                                                  f"activate commands")

    @commands.command(brief="Shows permissions for a user", aliases=['permissions'])
    @commands.guild_only()
    async def perms(self, ctx: codex.CodexContext, *, user: discord.User = None):
        user = user or ctx.author
        perms = '\n'.join(perm for perm, value in user.guild_permissions if value)
        await ctx.embed(title='Permissions for:', description=ctx.guild.name, author=user.display_name,
                        fields=[("\uFEFF", perms)], icon=user.avatar_url)

    @commands.has_permissions(manage_roles=True)
    @commands.command(brief="Creates a role with any name")
    @commands.guild_only()
    async def createrole(self, ctx: codex.CodexContext, *, rolename):
        await ctx.guild.create_role(name=rolename)
        await ctx.embed(title=f"{ctx.author.display_name} created the role, {rolename}, successfully")

    @commands.has_permissions(manage_messages=True)
    @commands.command(brief="Mutes a member")
    async def mute(self, ctx: codex.CodexContext, member: discord.Member, *, reason: Optional[str]):
        guild = ctx.guild
        user = member
        reason = reason or "they where being to loud"
        if member == ctx.message.author:
            await ctx.embed(title=f'**{ctx.message.author},** you cannot mute yourself, silly.')
        for role in guild.roles:
            if role.name == "Muted":
                if role in user.roles:
                    await ctx.embed(title="**{}** is already muted.".format(user))
        else:
            for role in guild.roles:
                if role.name == "Muted":
                    await member.add_roles(role)
                    if role in user.roles:
                        await ctx.embed(title=f"{ctx.author.display_name} muted {user.display_name} because {reason}")

    @commands.has_permissions(manage_messages=True)
    @commands.command(brief="Unmutes a member")
    async def unmute(self, ctx: codex.CodexContext, member: discord.Member):
        user = member
        muted = discord.utils.get(ctx.guild.roles, name="Muted")
        await user.remove_roles(muted)
        await ctx.embed(title=f"{user.display_name} was unmuted by {ctx.author.display_name}")


def setup(bot):
    bot.add_cog(Admin(bot))
