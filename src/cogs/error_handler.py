import discord

from discord.ext import commands


class ErrorHandler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, discord.DiscordException):
            await ctx.answer(str(error))
        else:
            self.bot.logger.error(str(error))


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
