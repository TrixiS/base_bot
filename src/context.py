import discord

from discord.ext import commands


class BotContext(commands.Context):

    ainit_tasks = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.phrases = self.bot.phrases
        self.guild_settings = {}

    async def __ainit__(self):
        for task in self.ainit_tasks:
            await task(self)

    async def answer(self, content):
        em = discord.Embed(
            description=content,
            colour=self.guild.me.colour
        )

        em.set_author(
            name=self.author.name,
            icon_url=self.author.avatar_url
        )

        await self.send(embed=em)
