import inspect

import discord
from discord.ext import commands

import codex


async def _can_run(_c: commands.Command, ctx):
    for check in _c.checks:
        try:
            if inspect.iscoroutinefunction(check):
                x = await check(ctx)
            else:
                x = check(ctx)
            if not x:
                return False
        except discord.DiscordException:
            return False
    else:
        return True


class Help(commands.Cog):

    def __init__(self, bot: codex.CodexBot):
        self.bot = bot

    @property
    def description(self):
        return "Help module"

    @commands.command(breif="Shows this command", aliases=["h"])
    async def help(self, ctx: codex.CodexContext, command: str = None):
        command_names_list = [x.name for x in self.bot.commands]
        if not command:
            return await ctx.embed(title="Help",
                                   fields=
                                   [("List of supported commands:",
                                     ", ".join([x.name for i, x in enumerate(self.bot.commands)])),
                                    ("Details", "Type `.help <command name>` for more details about each command.")],
                                   thumbnail=self.bot.user.avatar_url,
                                   not_inline=[0, 1])
        elif command in command_names_list:
            cmd: commands.Command = self.bot.get_command(command.lower())
            await ctx.embed(title=cmd.name,
                            fields=
                            [("Usage", f"{cmd.name} {cmd.signature}"),
                             ("About", cmd.brief),
                             ("Missing Permissions", "You are missing the permissions to run this command"
                             if not await _can_run(cmd, ctx) else "None"),
                             ("Aliases", ", ".join([f"`{a}`" for a in cmd.aliases]) if cmd.aliases else [])],
                            thumbnail=self.bot.user.avatar_url,
                            not_inline=[0, 1, 2, 4])
        else:
            return await ctx.send_error(f"Command `{command}` not found.")


def setup(bot):
    bot.add_cog(Help(bot))
