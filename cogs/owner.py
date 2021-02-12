import asyncio

import discord
from discord.ext import commands

from main import bot


class Owner(commands.Cog):

    def __init__(self, bot : commands.Bot):
        self.bot = bot

    @commands.is_owner()
    @commands.command(brief="Logs out the bot", aliases=["forcequit", "forcestop", "ddos"])
    async def die(self, ctx):
        user = ctx.message.author.display_name
        embed = discord.Embed(title=f"Codex has been forcefully stopped by {user}", color=discord.Color.random())
        for guild in bot.guilds:
            for channel in guild.channels:
                if channel.id == 803109205699461123:
                    await channel.send(embed=embed)
        await asyncio.sleep(1)
        await self.bot.logout()

    @commands.is_owner()
    @commands.command()
    async def load(self, ctx, extension):
        try:
            self.bot.load_extension(extension)
            await ctx.send(f"{extension} loaded")
        except commands.ExtensionError as e:
            await ctx.send(f"{e.__class__.__name__}: {e}")

    @commands.is_owner()
    @commands.command()
    async def unload(self, ctx, extension):
        try:
            self.bot.unload_extension(extension)
            await ctx.send(f"{extension} unloaded")
        except commands.ExtensionError as e:
            await ctx.send(f"{e.__class__.__name__}: {e}")

    @commands.is_owner()
    @commands.command()
    async def reload(self, ctx, extension):
        try:
            self.bot.reload_extension(extension)
            await ctx.send(f"{extension} reloaded")
        except commands.ExtensionError as e:
            await ctx.send(f"{e.__class__.__class__}: {e}")

    @commands.is_owner()
    @commands.command(aliases=["echo"])
    async def say(self, ctx, *, message):
        await ctx.message.delete()
        await ctx.send(message)            

def setup(bot):
    bot.add_cog(Owner(bot))
