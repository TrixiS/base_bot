import logging

from discord.ext import commands

from .context import BotContext
from .services.service import BotService


class Bot(commands.AutoShardedBot):

    def __init__(self, *args, **kwargs):
        super().__init__(
            command_prefix=self.config.command_prefixes,
            intents=self.config.discord_intents
        )
        self.logger = logging.getLogger("Bot")
        self.ctx_cls = kwargs.get("ctx_cls", BotContext)
        self.services = []

    def run(self):
        super().run(self.config.bot_token, bot=True)

    def load_cogs(self, cogs, reload=False):
        for cog in cogs:
            try:
                if reload and cog in self.extensions:
                    self.unload_extension(cog)

                self.load_extension(cog)
                self.logger.info(self.phrases.loaded_cog.format(cog))
            except Exception as e:
                self.logger.error(self.phrases.loading_failed.format(cog, str(e)))

    def add_service(self, service):
        if not issubclass(service, BotService):
            return self.logger.error(f"Got {service.__name__}. BotService expected.")

        self.services.append(service(self))

    async def close(self):
        for service in self.services:
            await service.close()

        await super().close()

    async def is_owner(self, user):
        app = await self.application_info()

        if app.team is not None:
            return any(m.id == user.id for m in app.team.members) or app.owner.id == user.id

        return app.owner.id == user.id

    async def process_commands(self, message):
        ctx = await self.get_context(message, cls=self.ctx_cls)

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
        from . import phrases
        return phrases
