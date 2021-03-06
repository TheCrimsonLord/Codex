import random
from typing import Optional

import aiohttp
import discord
from discord.ext import commands

import codex
from codex.custom_context import text_to_owo
from games.ttt import TicTacToe


class Fun(commands.Cog):

    def __init__(self, bot: codex.CodexBot):
        self.bot = bot

    @property
    def description(self):
        return "Fun little command"

    @commands.command(brief="Sends the latency of the bot")
    async def ping(self, ctx: codex.CodexContext):
        await ctx.embed(title=f"Pong {round(self.bot.latency * 1000)}ms")

    @commands.command(name="8ball", brief="Ask and you shall receive ")
    async def _8ball(self, ctx: codex.CodexContext, *, question):
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
        await ctx.embed(title=question, description=random.choice(responses))

    @commands.command(aliases=["memes", "reddit"], brief="Sends a hot post from any subreddit")
    async def meme(self, ctx: codex.CodexContext, subreddit: Optional[str]):
        subreddit = subreddit or "memes"
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"https://www.reddit.com/r/{subreddit}/hot.json?sort=hot") as r:
                res = await r.json()
        data = res["data"]["children"][random.randint(0, 25)]["data"]
        desc = data['selftext'] or None
        reddit_title = data["title"]
        reddit_link = data["permalink"]
        if data["over_18"]:
            if ctx.channel.is_nsfw():
                await ctx.embed(title=reddit_title, description=desc, title_url=f"https://reddit.com{reddit_link}",
                                image=data["url"], footer=f"👍{data['ups']} | 💬{data['num_comments']}")
            else:
                await ctx.embed(title=f'**{ctx.channel}** is not a NSFW channel')
        else:
            await ctx.embed(title=reddit_title, description=desc, title_url=f"https://reddit.com{reddit_link}",
                            image=data["url"], footer=f"👍{data['ups']} | 💬{data['num_comments']}")

    @commands.command(brief="Clones your friends")
    async def clone(self, ctx: codex.CodexContext, user: discord.User):
        await ctx.embed(title=f"Cloning Processes of {user.display_name} Complete", image_url=user.avatar_url)

    @commands.command(breif="Sends a random death message", aliases=["murder"])
    async def kill(self, ctx: codex.CodexContext, user: discord.User):
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
        await ctx.embed(title=f"{random.choice(outcome)}")

    @commands.command(brief="Allows you to make the bot say whatever you want", aliases=["echo"])
    async def say(self, ctx: codex.CodexContext, *, message):
        await ctx.message.delete()
        await ctx.embed(title=message)

    @commands.command(brief="Turns any message to owo")
    async def owo(self, ctx: codex.CodexContext, *, msg):
        await ctx.embed(title=text_to_owo(msg))

    @commands.command(brief="Play tic tac toe", aliases=["ttt"])
    async def tictactoe(self, ctx: codex.CodexContext):
        await TicTacToe(ctx).play()


def setup(bot):
    bot.add_cog(Fun(bot))
