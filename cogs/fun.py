import random
from typing import Optional

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

    @commands.command(aliases=["memes", "reddit"])
    async def meme(self, ctx, subreddit: Optional[str]):
        subreddit = subreddit or "memes"
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"https://www.reddit.com/r/{subreddit}/hot.json?sort=hot") as r:
                res = await r.json()
        data = res["data"]["children"][random.randint(0, 25)]["data"]
        desc = data['selftext'] or None
        reddit_title = data["title"]
        reddit_link = data["permalink"]
        embed = discord.Embed(title=reddit_title, description=desc, url=f"https://reddit.com{reddit_link}",
                              color=discord.Color.random())
        embed.set_image(url=data["url"])
        embed.set_footer(text=f"👍{data['ups']} | 💬{data['num_comments']}")
        if data["over_18"]:
            if ctx.channel.is_nsfw():
                await ctx.send(embed=embed)
            else:
                await ctx.send(f'**{ctx.channel}** is not a NSFW channel')
        else:
            await ctx.send(embed=embed)

    @commands.command()
    async def clone(self, ctx, user: discord.User):
        embed = discord.Embed(title=f"Cloning Processes of {user.display_name} Complete", color=discord.Color.random())
        embed.set_image(url=user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(breif="Sends a random death message", aliases=["murder"])
    async def kill(self, ctx, user: discord.User):
        author = ctx.author.display_name
        usr = user.display_name
        outcome = [f"was shot.",
                   f"{author} stabbed {usr} in the chest",
                   f"{usr} dodged the attack",
                   f"{usr} was run over by a car",
                   f"{usr} was shot by a tank",
                   f"{author} called in a tactical nuke\nto be dropped on them",
                   f"{author} tried to stab {usr} and\ngot called the cops on themselves",
                   f"{usr} shot you instead"]
        embed = discord.Embed(title=f"{random.choice(outcome)}", color=discord.Color.random())
        await ctx.send(embed=embed)

    @commands.command(aliases=["echo"])
    async def say(self, ctx, *, message):
        await ctx.message.delete()
        await ctx.send(message, allowed_mentions=discord.AllowedMentions.none())


def setup(bot):
    bot.add_cog(Fun(bot))
