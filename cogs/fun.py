import random

import aiohttp
import discord
from discord.ext import commands


class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        embed = discord.Embed(title=f"Pong {round(self.bot.latency * 1000)}ms", color=discord.Color.random())
        await ctx.send(embed=embed)

    @commands.command(name="8ball", brief="Ask and you shall receive ")
    async def _8ball(self, ctx, *, question):
        responses = ["It is certain",
                     "It is decidedly so.",
                     "Without a doubt.",
                     "Yes - definitely.",
                     "You may rely on it.",
                     "As I see it, yes.",
                     "Most likely.",
                     "Outlook good.",
                     "Yes.",
                     "Maybe?",
                     "Signs point to yes.",
                     "Reply hazy, try again.",
                     "Ask again later.",
                     "Better not tell you now.",
                     "Cannot predict now.",
                     "Concentrate and ask again.",
                     "Don't count on it.",
                     "My reply is no.",
                     "My sources say no.",
                     "Outlook not so good.",
                     "Very doubtful."]
        embed = discord.Embed(title=question, description=random.choice(responses), color=discord.Color.random())
        await ctx.send(embed=embed, allowed_mentions=discord.AllowedMentions.none())

    @commands.command(aliases=["memes"])
    async def meme(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://www.reddit.com/r/memes/new.json?sort=hot") as r:
                res = await r.json()
        data2 = res["data"]["children"][random.randint(0, 24)]["data"]
        reddit_title = data2["title"]
        embed = discord.Embed(title=reddit_title, color=discord.Color.random())
        embed.set_image(url=data2["url"])
        await ctx.send(embed=embed)

    @commands.command()
    async def clone(self, ctx, user: discord.User):
        embed = discord.Embed(title=f"Cloning Processes of {user.display_name} Complete", color=discord.Color.random())
        embed.set_image(url=user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(breif="Sends a random death message", aliases=["murder"])
    async def kill(self, ctx, user: discord.User):
        outcome = ["was shot.",
                   "was stabbed in the chest.",
                   "dodged the attack."]
        embed = discord.Embed(title=f"{user.display_name} {random.choice(outcome)}", color=discord.Color.random())
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Fun(bot))
