import asyncio

from discord.ext import commands


class Owner(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.is_owner()
    @commands.command(brief="Log out")
    async def die(self, ctx):
        await ctx.send("Bye :(")
        await asyncio.sleep(5)
        await self.bot.logout()


def setup(bot):
    bot.add_cog(Owner(bot))
