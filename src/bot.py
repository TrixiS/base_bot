import logging

from discord.ext import commands

from .context import BotContext


class Bot(commands.AutoShardedBot):

    def __init__(self, *args, **kwargs):
        super().__init__(
            command_prefix=self._get_command_prefix,
            intents=self.config.discord_intents
        )
        self.logger = logging.getLogger("Bot")
        self.ctx_cls = kwargs.get("ctx_cls", BotContext)
        self.services = []

    @staticmethod
    async def _get_command_prefix(bot, message):
        default_prefixes = bot.config.command_prefixes + [bot.user.mention]

        if message.guild is None:
            return default_prefixes

        prefix_doc = await bot.db.guild_settings.find_one(
            {"guild_id": message.guild.id},
            {"prefix": 1}
        )

        if prefix_doc is None or "prefix" not in prefix_doc:
            return default_prefixes
        else:
            return [prefix_doc["prefix"], bot.user.mention]

    def run(self):
        super().run(self.config.bot_token, bot=True)

    def load_cogs(self, cogs, reload=False):
        for cog in cogs:
            if reload and cog in self.extensions:
                self.unload_extension(cog)

            self.load_extension(cog)

    async def close(self):
        for service in self.services:
            await service.close()

        await super().close()

    async def is_owner(self, user):
        app = await self.application_info()

        if app.team is not None:
            return any(m.id == user.id for m in app.team.members) or app.owner.id == user.id

        return app.owner.id == user.id

    async def get_context(self, message):
        ctx = await super().get_context(message, cls=self.ctx_cls)
        await ctx.__ainit__()
        return ctx

    async def process_commands(self, message):
        ctx = await self.get_context(message)

        if ctx.command is None or ctx.author.bot:
            return

        await self.invoke(ctx)

    async def on_message(self, message):
        if message.author.bot or message.guild is None:
            return

        await self.process_commands(message)

    async def on_ready(self):
        print(self.phrases.started.format(self.user.name))

    @property
    def config(self):
        from . import config
        return config

    @property
    def phrases(self):
        from .phrases import ru
        return ru
