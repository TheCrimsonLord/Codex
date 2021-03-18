import json
import os
import platform

import discord
import dotenv
from discord.ext import commands

import codex


def get_prefix(_bot, message):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)
    if not message.guild:
        return commands.when_mentioned_or(".")(bot, message)
    else:
        return commands.when_mentioned_or(prefixes.get(str(message.guild.id), "."))(bot, message)


bot = codex.CodexBot(command_prefix=get_prefix, help_command=None)


@bot.event
async def on_guild_join(guild):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)
    prefixes[str(guild.id)] = "."
    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)


@bot.event
async def on_guild_remove(guild):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)
    prefixes.pop(str(guild.id))
    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online,
                              activity=discord.Activity(type=discord.ActivityType.watching, name="Codex be created"))
    print(f"Bot online as {bot.user}.")
    print(f"Discord {discord.__version__}")
    print(f"Python {platform.python_version()}")
    print(f"I'm in {str(len(bot.guilds))} servers")
    print(f"Loaded {str(len(bot.cogs))} cogs")


for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

dotenv.load_dotenv()
bot.run(os.getenv("TOKEN"))
