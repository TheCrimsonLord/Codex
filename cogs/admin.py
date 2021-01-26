import typing

import discord
from discord.ext import commands


class Admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount + 1)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=f"{ctx.author} | {reason}")
        await ctx.send(f"Banned {member} for {reason}")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=f"{ctx.author} | {reason}")
        await ctx.send(f"Banned {member} for {reason}")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def unban(self, ctx, *, member: typing.Union[int, str]):
        banned_users = await ctx.guild.bans()

        for ban_entry in banned_users:
            if (isinstance(member, int) and ban_entry.user.id == member) or \
                    (isinstance(member, str) and member in str(ban_entry.user)):
                await ctx.guild.unban(ban_entry.user, reason=str(ctx.author))
                return await ctx.send(f"Unbanned {ban_entry.user}")


def setup(bot):
    bot.add_cog(Admin(bot))
