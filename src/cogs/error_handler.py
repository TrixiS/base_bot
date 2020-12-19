import discord
import sys
import traceback

from discord.ext import commands


class ErrorHandler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandError):
            await ctx.answer(str(error))
        else:
            self.bot.logger.error(traceback.format_exception(type(error), error, error.__traceback__, file=sys.stderr))


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
