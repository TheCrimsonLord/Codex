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

    async def on_message(self, message: discord.Message):
        ctx: codex.CodexContext = await self.get_context(message, cls=codex.CodexContext)
        await self.invoke(ctx)
