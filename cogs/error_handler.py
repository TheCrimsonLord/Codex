import sys
import traceback

import discord
from discord.ext import commands


class CommandErrorHandler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """The event triggered when an error is raised while invoking a command.
        Parameters
        ------------
        ctx: commands.Context
            The context used for command invocation.
        error: commands.CommandError
            The Exception raised.
        """

        # This prevents any commands with local handlers being handled here in on_command_error.
        if hasattr(ctx.command, "on_error"):
            return

        if isinstance(error, commands.BadArgument):
            embed = discord.Embed(title=f"You passed in a bad argument\n{error}", description=None, color=discord.Color.random())
            await ctx.send(embed=embed, content=None)

        if isinstance(error, (commands.MissingPermissions, commands.BotMissingPermissions)):
            embed = discord.Embed(title=str(error), description=None, color=discord.Color.random())
            await ctx.send(embed=embed, content=None)

        if isinstance(error, commands.CommandNotFound):
            embed = discord.Embed(title="Invalid command used.", description=None, color=discord.Color.random())
            await ctx.send(embed=embed, content=None)

        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Missing Requirements.", description=None, color=discord.Color.random())
            await ctx.send(embed=embed, content=None)

        # This prevents any cogs with an overwritten cog_command_error being handled here.
        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:  # noqa
                return

        ignored = (commands.CommandNotFound,)

        # Allows us to check for original exceptions raised and sent to CommandInvokeError.
        # If nothing is found. We keep the exception passed to on_command_error.
        error = getattr(error, "original", error)

        # Anything in ignored will return and prevent anything happening.
        if isinstance(error, ignored):
            return

        if isinstance(error, commands.DisabledCommand):
            embed = discord.Embed(title=f"{ctx.command} has been disabled.", description=None, color=discord.Color.random())
            await ctx.send(embed=embed, content=None)

        elif isinstance(error, commands.NoPrivateMessage):
            embed = discord.Embed(title=f"{ctx.command} can not be used in Private Messages.", description=None, color=discord.Color.random())
            try:
                await ctx.send(embed=embed, content=None)
            except discord.HTTPException:
                pass

        # For this error example we check to see where it came from...
        elif isinstance(error, commands.BadArgument):
            embed = discord.Embed(title="I could not find that member. Please try again.", description=None, color=discord.Color.random())
            await ctx.send(embed=embed, content=None)

        else:
            # All other Errors not returned come here. And we can just print the default TraceBack.
            print("Ignoring exception in command {}:".format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    """Below is an example of a Local Error Handler for our command do_repeat"""

    @commands.command(name="repeat", aliases=["mimic", "copy"])
    async def do_repeat(self, ctx, *, inp: str):
        embed = discord.Embed(title=inp, description=None, color=discord.Color.random())
        await ctx.send(embed=embed, content=None)

    @do_repeat.error
    async def do_repeat_handler(self, ctx, error):
        """A local Error Handler for our command do_repeat.
        This will only listen for errors in do_repeat.
        The global on_command_error will still be invoked after.
        """

        # Check if our required argument inp is missing.
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == "inp":
                embed = discord.Embed(title="You forgot to give me input to repeat!", description=None,
                                      color=discord.Color.random())
            await ctx.send(embed=embed, content=None)


def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))