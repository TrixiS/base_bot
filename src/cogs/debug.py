import discord
import ast

from discord.ext import commands
from .utils.checks import is_owner


def insert_returns(body):
	if isinstance(body[-1], ast.Expr):
		body[-1] = ast.Return(body[-1].value)
		ast.fix_missing_locations(body[-1])
	if isinstance(body[-1], ast.If):
		insert_returns(body[-1].body)
		insert_returns(body[-1].orelse)
	if isinstance(body[-1], ast.With):
		insert_returns(body[-1].body)


class DebugCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @is_owner()
    @commands.command()
    async def load(self, ctx, *, cog: str):
        try:
            self.bot.load_extension(cog)
            await ctx.send(f"{cog} unloaded")
        except Exception as e:
            await ctx.send(str(e))

    @is_owner()
    @commands.command()
    async def unload(self, ctx, *, cog: str):
        try:
            self.bot.unload_extension(cog)
            await ctx.send(f"{cog} loaded")
        except Exception as e:
            await ctx.send(str(e))

    @is_owner()
    @commands.command()
    async def reload(self, ctx, *, cog: str):
        try:
            self.bot.reload_extension(cog)
            await ctx.send(f"{cog} reloaded")
        except Exception as e:
            await ctx.send(str(e))

    @is_owner()
    @commands.command()
    async def eval(self, ctx, *, code: str):
        fn_name = "_eval_expr"

        cmd = code.strip('` ')
        cmd = '\n'.join(f"	{i}" for i in cmd.splitlines())
        body = f"async def {fn_name}():\n{cmd}"

        parsed = ast.parse(body)
        body = parsed.body[0].body

        insert_returns(body)

        env = {
            "bot": ctx.bot,
            "discord": discord,
            "command": discord.ext.commands,
            "ctx": ctx,
            "__import__": __import__,
            "__name__": __name__
        }

        exec(compile(parsed, filename="<ast>", mode="exec"), env)

        fmt = "```Python\n{}```"

        try:
            result = (await eval(f"{fn_name}()", env))
            await ctx.send(fmt.format(result))
        except Exception as e:
            await ctx.send(fmt.format(f"{type(e).__name__}: {str(e)}"))

    @is_owner()
    @commands.command()
    async def kill(self, ctx):
        await ctx.send(ctx.phrases.kill)
        await self.bot.close()


def setup(bot):
    bot.add_cog(DebugCog(bot))
