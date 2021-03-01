import asyncio

import discord
from discord.ext import commands

import codex


class Owner(commands.Cog):

    def __init__(self, bot: codex.CodexBot):
        self.bot = bot

    @commands.is_owner()
    @commands.command(brief="Logs out the bot", aliases=["forcequit", "forcestop", "ddos"])
    async def die(self, ctx: codex.CodexContext):
        await ctx.embed(title="Mr. Stark?", clr=discord.Colour.red())
        await asyncio.sleep(.5)
        await ctx.embed(title="I don't feel so good...", clr=discord.Colour.blue())
        await asyncio.sleep(1)
        await self.bot.logout()

    @commands.is_owner()
    @commands.command(brief="Loads a cog")
    async def load(self, ctx: codex.CodexContext, extension):
        try:
            self.bot.load_extension(extension)
            await ctx.embed(title=f"{extension} loaded")
        except commands.ExtensionError as e:
            await ctx.embed(title=f"{e.__class__.__name__}: {e}")

    @commands.is_owner()
    @commands.command(brief="Unloads a cog")
    async def unload(self, ctx: codex.CodexContext, extension):
        try:
            self.bot.unload_extension(extension)
            await ctx.embed(title=f"{extension} unloaded")
        except commands.ExtensionError as e:
            await ctx.embed(title=f"{e.__class__.__name__}: {e}")

    @commands.is_owner()
    @commands.command(brief="Reloads a cog")
    async def reload(self, ctx: codex.CodexContext, extension):
        try:
            self.bot.reload_extension("cogs.{extension}")
            await ctx.embed(title=f"{extension} reloaded")
        except commands.ExtensionError as e:
            await ctx.embed(title=f"{e.__class__.__class__}: {e}")


def setup(bot):
    bot.add_cog(Owner(bot))
