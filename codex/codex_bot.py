import discord
from discord.ext import commands

import codex


class CodexBot(commands.Bot):

    async def on_message(self, message: discord.Message):
        ctx: codex.CodexContext = await self.get_context(message, cls=codex.CodexContext)
        await self.invoke(ctx)
