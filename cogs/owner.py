import asyncio
from discord.ext import commands


class Owner(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.is_owner()
    @commands.command(brief="Logs out the bot", aliases=["forcequit", "forcestop", "ddos"])
    async def die(self):
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
            self.bot.reload_extension("cogs.{extension}")
            await ctx.send(f"{extension} reloaded")
        except commands.ExtensionError as e:
            await ctx.send(f"{e.__class__.__class__}: {e}")


def setup(bot):
    bot.add_cog(Owner(bot))
