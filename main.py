import json
import os

import discord
import dotenv
from discord.ext import commands


def get_prefix(bot, message):  # noqa
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)
    return commands.when_mentioned_or(prefixes.get(str(message.guild.id), "."))(bot, message)


bot = commands.Bot(command_prefix=get_prefix)
bot.remove_command("help")


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
                              activity=discord.Activity(type=discord.ActivityType.watching, name="The World Burn"))
    print(f"Bot online as {bot.user}.")
    print(discord.version_info)
    print("I'm in " + str(len(bot.guilds)) + " servers")


for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")


@commands.is_owner()
@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')  # loads the extension in the "cogs" folder
    embed = discord.Embed(title=f"Loaded {extension}", color=discord.Color.random())
    await ctx.send(embed=embed)


@commands.is_owner()
@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    embed = discord.Embed(title=f"Unloaded {extension}", color=discord.Color.random())
    await ctx.send(embed=embed)
    return


@commands.is_owner()
@bot.command()
async def reload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    bot.load_extension(f'cogs.{extension}')
    embed = discord.Embed(title=f"Reloaded {extension}", color=discord.Color.random())
    await ctx.send(embed=embed)
    return


dotenv.load_dotenv()
bot.run(os.getenv("TOKEN"))
