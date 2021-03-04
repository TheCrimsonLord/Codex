import asyncio
import io
import random
from typing import Union, List, Tuple, Callable

import discord
from PIL.Image import Image
from discord.ext import commands


async def notify_user(user, message):
    if user is not None:
        channel = user.dm_channel
        if channel is None:
            channel = await user.create_dm()
        await channel.send(message)


vowels = ['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U']


def last_replace(s, old, new):
    li = s.rsplit(old, 1)
    return new.join(li)


def text_to_owo(text):
    """ Converts your text to OwO """
    smileys = [';;w;;', '^w^', '>w<', 'UwU', '(・`ω´・)', '(´・ω・`)']

    text = text.replace('L', 'W').replace('l', 'w')
    text = text.replace('R', 'W').replace('r', 'w')

    text = last_replace(text, '!', '! {}'.format(random.choice(smileys)))
    text = last_replace(text, '?', '? owo')
    text = last_replace(text, '.', '. {}'.format(random.choice(smileys)))

    for v in vowels:
        if 'n{}'.format(v) in text:
            text = text.replace('n{}'.format(v), 'ny{}'.format(v))
        if 'N{}'.format(v) in text:
            text = text.replace('N{}'.format(v), 'N{}{}'.format(
                'Y' if v.isupper() else 'y', v))

    return text


def _wrap_user(user: discord.abc.User):
    return f"**{user}** "


class CodexContext(commands.Context):
    INFO = 0

    async def trash_reaction(self, message: discord.Message):
        if len(message.embeds) == 0:
            return

        def check(_reaction: discord.Reaction, _user: Union[discord.User, discord.Member]):
            return all([
                _user.id == self.author.id or _user.guild_permissions.manage_messages,
                _reaction.message.id == message.id,
                str(_reaction) == "🗑️"
            ])

        await message.add_reaction("🗑️")
        await asyncio.sleep(0.5)
        try:
            _, _ = await self.bot.wait_for("reaction_add", timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await message.clear_reactions()
        else:
            await message.delete()

    async def send_ok(self, message: str, *, user: discord.abc.User = None,
                      title: str = None, trash: bool = False, ping: bool = False):
        if not user:
            user = self.author
        msg = await self.send(
            user.mention if ping else None,
            embed=discord.Embed(
                title=title,
                description=f"{_wrap_user(user) if user else ''}{message}",
                color=discord.Color.random()
            ))
        if trash:
            await self.trash_reaction(msg)
        else:
            return msg

    async def send_error(self, message: str, *, user: discord.abc.User = None,
                         title: str = None, trash: bool = False, ping: bool = False):
        if not user:
            user = self.author
        msg = await self.send(
            user.mention if ping else None,
            embed=discord.Embed(
                title=title,
                description=f"{_wrap_user(user) if user else ''}{message}",
                color=discord.Color.random()
            ))
        if trash:
            await self.trash_reaction(msg)
        else:
            return msg

    async def embed(self, *,
                    author: str = None,
                    description: str = None,
                    title: str = None,
                    title_url: str = None,
                    typ: int = INFO,
                    fields: List[Tuple[str, str]] = None,
                    thumbnail: str = None,
                    clr: discord.Colour = None,
                    image: Union[str, io.BufferedIOBase] = None,
                    footer: str = None,
                    not_inline: List[int] = [],
                    trash_reaction: bool = False,
                    mentions: str = None,
                    icon: str = None):
        if typ and clr:
            raise ValueError("typ and clr can not be both defined")
        embed = discord.Embed(
            title=title,
            description=description,
            color=clr or discord.Color.random(),
            title_url=title_url,
            allowed_mentions=mentions or discord.AllowedMentions.none()
        )
        if author:
            embed.set_author(name=author)
        if icon:
            embed.set_author(name=author, icon_url=icon)
        if image:
            if isinstance(image, str):
                embed.set_image(url=image)
                f = None
            elif isinstance(image, Image):
                buf = io.BytesIO()
                image.save(buf, "png")
                buf.seek(0)
                f = discord.File(buf, filename="image.png")
                embed.set_image(url="attachment://image.png")
            else:
                image.seek(0)
                f = discord.File(image, filename="image.png")
                embed.set_image(url="attachment://image.png")
        else:
            f = None
        if footer:
            embed.set_footer(text=footer)
        if thumbnail:
            embed.set_thumbnail(url=thumbnail)
        for n, r in enumerate(fields or []):
            embed.add_field(name=r[0], value=r[1] or "None", inline=n not in not_inline)
        msg = await self.send(embed=embed, file=f)
        if trash_reaction:
            await self.trash_reaction(msg)
        else:
            return msg

    async def input(self, typ: type, cancel_str: str = "cancel", ch: Callable = None, err=None, check_author=True,
                    return_author=False, del_error=60, del_response=False, timeout=60.0):
        def check(m):
            return ((m.author == self.author and m.channel == self.channel) or not check_author) and not m.author.bot

        while True:
            try:
                inp: discord.Message = await self.bot.wait_for('message', check=check, timeout=timeout)
                if del_response:
                    await inp.delete()
                if inp.content.lower() == cancel_str.lower():
                    return (None, None) if return_author else None
                res = typ(inp.content.lower())
                if ch:
                    if not ch(res):
                        raise ValueError
                return (res, inp.author) if return_author else res
            except ValueError:
                await self.send(err or "That's not a valid response, try again" +
                                ("" if not cancel_str else f" or type `{cancel_str}` to quit"),
                                delete_after=del_error)
                continue
            except asyncio.TimeoutError:
                await self.send("You took too long to respond ): Try to start over", delete_after=del_error)
                return (None, None) if return_author else None
