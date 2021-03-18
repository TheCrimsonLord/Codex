import logging

import discord
from discord.ext import commands

import codex

log = logging.getLogger(__name__)


class ErrorHandler(commands.Cog):
    """Handler for discord.py errors."""

    def __init__(self, bot: codex.CodexBot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(
            self, ctx: codex.CodexContext, error: commands.CommandError
    ):
        """Handle errors caused by commands."""
        # Skips errors that were already handled locally.
        if getattr(ctx, "handled", False):
            return

        ignored = commands.CommandNotFound

        if isinstance(error, ignored):
            return

        if isinstance(error, commands.NoPrivateMessage):
            await ctx.embed(title="This Command Cannot Be Used In Private DMS")

        elif isinstance(error, commands.TooManyArguments):
            await ctx.embed(title="You Passed In Too Many Arguments")

        elif isinstance(error, commands.NSFWChannelRequired):
            await ctx.embed(title=f"**{ctx.channel}** is not a NSFW channel")

        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.embed(title=f"You are missing some required arguments\n`{error.param.name}`")

        elif isinstance(error, commands.NotOwner):
            await ctx.embed(title=str(error))

        elif isinstance(error, commands.MissingPermissions):
            await ctx.embed(title=str(error))

        elif isinstance(error, commands.CommandOnCooldown) or isinstance(
                error, commands.CheckFailure
        ):
            await ctx.embed(title=str(error))

        elif isinstance(error, commands.DisabledCommand):  # SoonTM
            await ctx.embed(title="This command is disabled")

        elif isinstance(error, commands.BadArgument):
            await ctx.embed(title=f"You passed in a bad argument\n{error}")

        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.embed(title=str(error))

        elif isinstance(error, commands.CommandInvokeError):
            await ctx.embed(title="If you are getting this error, contact TheCrimsonLord#3794 for help.\nThis is due "
                                  "to the fact he is a terrible coder")
            log.error(
                f"{ctx.command.qualified_name} failed to execute. ",
                exc_info=error.original)
            embed = discord.Embed(title="AHHH!", description=(f"""You idiot coder.\n
                        **{ctx.author}** tried to run **{ctx.command.name}** in **{ctx.guild}** and it errored out 
                        because you're dumb\n error:\n{error}"""), color=discord.Color.red())
            for guild in self.bot.guilds:
                for channel in guild.channels:
                    if channel.id == 816183861893398548:
                        await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
