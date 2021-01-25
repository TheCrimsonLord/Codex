import json
import os

import discord
import dotenv
from discord.ext import commands


def get_prefix(bot, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]


bot = commands.Bot(command_prefix=get_prefix)

bot.remove_command("help")


@bot.group()
async def help(ctx):
    em = discord.Embed(title="Help", description="Use .help <command> for extended information on a command.",
                       color=ctx.author.color)
    em.add_field(name="Moderation", value="kick,ban,unban,clear,changeprefix")
    em.add_field(name="Fun", value="8ball")
    await ctx.send(embed=em)


@bot.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = '.'

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)


@bot.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)


@bot.command()
async def changeprefix(ctx, prefix):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

    await ctx.send(f'Prefix changed to: {prefix}')


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online,
                              activity=discord.Activity(type=discord.ActivityType.watching, name="The World End"))
    print(f"Bot online as {bot.user}.")


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


@bot.command()
async def load(extension):
    bot.load_extension(f'cogs.{extension}')


@bot.command()
async def unload(extension):
    bot.unload_extension(f'cogs.{extension}')


dotenv.load_dotenv()
bot.run(os.getenv("TOKEN"))
