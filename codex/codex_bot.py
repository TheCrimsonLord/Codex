from datetime import datetime

import discord
from discord.ext import commands

import codex


class FakeUser(discord.User):
    def __init__(self, *, state, data):
        super().__init__(state=state, data=data)
        self.name = ""


class CodexBot(commands.Bot):

    def __init__(self, *args, **kwargs):
        super(CodexBot, self).__init__(*args, **kwargs)
        self.TRACE = 7
        self.messages = 0
        self.commands_executed = 0
        self.start_time = datetime.now()
        self.commands_ran = {}

        async def command_ran(ctx: codex.CodexContext):
            self.commands_executed += 1
            if ctx.command.qualified_name not in self.commands_ran:
                self.commands_ran[ctx.command.qualified_name] = 1
            else:
                self.commands_ran[ctx.command.qualified_name] += 1

        self.add_listener(
            command_ran,
            "on_command_completion"
        )

    async def on_message(self, message: discord.Message):
        ctx: codex.CodexContext = await self.get_context(message, cls=codex.CodexContext)
        await self.invoke(ctx)
        if not ctx.command and not message.author.bot and message.guild:
            self.messages += 1
