import datetime as dt
import json
import typing
import discord
from discord.ext import commands


class Admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="Clears messages", aliases=["purge"])
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int = 5):
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
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        embed = discord.Embed(title=f"{ctx.author} kicked {member} for {reason}", color=discord.Color.random())
        await member.kick(reason=f"{ctx.author} | {reason}")
        await ctx.send(embed=embed)

    @commands.command(brief="Bans members", aliases=["permkick"])
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        embed = discord.Embed(title=f"{ctx.author} banned {member} for {reason}", color=discord.Color.random())
        await member.ban(reason=f"{ctx.author} | {reason}")
        await ctx.send(embed=embed)

    @commands.command(brief="Unbans members")
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def unban(self, ctx, *, member: typing.Union[int, str]):
        banned_users = await ctx.guild.bans()
        for ban_entry in banned_users:
            if (isinstance(member, int) and ban_entry.user.id == member) or \
                    (isinstance(member, str) and member in str(ban_entry.user)):
                await ctx.guild.unban(ban_entry.user, reason=str(ctx.author))
                embed = discord.Embed(title=f"{ctx.author} unbanned {ban_entry.user}", color=discord.Color.random())
                return await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def setrules(self, ctx, *, inp: str):
        amount: int = 1
        embed = discord.Embed(title="Rules", description=inp, color=discord.Color.random())
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
        await ctx.send(embed=embed)

    @commands.command(brief="Changes the command prefix", aliases=["cp"])
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def changeprefix(self, ctx, prefix):
        with open("prefixes.json", "r") as f:
            prefixes = json.load(f)
        prefixes[str(ctx.guild.id)] = prefix
        with open("prefixes.json", "w") as f:
            json.dump(prefixes, f, indent=4)
        embed = discord.Embed(title="Prefix has successfully been changed", description=f"You can now use {prefix} to "
                                                                                        f"activate commands",
                              color=discord.Color.random())
        await ctx.send(embed=embed)

    @commands.command(aliases=['perms_for', 'permissions'])
    @commands.guild_only()
    async def perms(self, ctx, *, member: discord.Member = None):
        if not member:
            member = ctx.author
        perms = '\n'.join(perm for perm, value in member.guild_permissions if value)
        embed = discord.Embed(title='Permissions for:', description=ctx.guild.name, color=discord.Color.random())
        embed.set_author(icon_url=member.avatar_url, name=str(member.display_name))
        embed.add_field(name='\uFEFF', value=perms)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def createrole(self, ctx, *, rolename):
        await ctx.guild.create_role(name=rolename)
        embed = discord.Embed(title=f"{ctx.author.display_name} created the role, {rolename}, successfully",
                              color=discord.Color.random())
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Admin(bot))
