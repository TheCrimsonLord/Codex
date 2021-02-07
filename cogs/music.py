import os

import discord
import youtube_dl
from discord.ext import commands

from main import bot


class Music(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def play(self, ctx, url: str):
        song_there = os.path.isfile("song.mp3")
        try:
            if song_there:
                os.remove("song.mp3")
        except PermissionError:
            embed = discord.Embed(title="Wait for the current playing music to end or use the 'stop' command",
                                  color=discord.Color.random())
            await ctx.send(embed=embed)
            return

        voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
        await voiceChannel.connect()
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.rename(file, "song.mp3")
        voice.play(discord.FFmpegPCMAudio("song.mp3"))

    @commands.command(aliases=["fuckoff"])
    async def leave(self, ctx):
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if voice.is_connected():
            await voice.disconnect()
        else:
            embed = discord.Embed(title="The bot is not connected to a voice channel.", color=discord.Color.random())
            await ctx.send(embed=embed)

    @commands.command()
    async def pause(self, ctx):
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            voice.pause()
        else:
            embed = discord.Embed(title="Currently no audio is playing.", color=discord.Color.random())
            await ctx.send(embed=embed)

    @commands.command()
    async def resume(self, ctx):
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if voice.is_paused():
            voice.resume()
        else:
            embed = discord.Embed(title="The audio is not paused.", color=discord.Color.random())
            await ctx.send(embed=embed)

    @commands.command()
    async def stop(self, ctx):
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        voice.stop()


def setup(bot):
    bot.add_cog(Music(bot))
