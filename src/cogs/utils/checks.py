from discord.ext import commands


def is_owner():

    async def predicate(ctx):
        if not await ctx.bot.is_owner(ctx.author):
            raise commands.CheckFailure(ctx.phrases.not_owner)

        return True

    return commands.check(predicate)
