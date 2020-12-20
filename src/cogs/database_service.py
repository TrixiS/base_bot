from motor.motor_asyncio import AsyncIOMotorClient
from .utils.cog_services import ServiceCog


class DatabaseService(ServiceCog):

    def __init__(self, bot, *args, **kwargs):
        super().__init__(bot)
        database_name = kwargs.pop("database_name", "bot")
        self.mongo_client = AsyncIOMotorClient(*args, **kwargs)
        self.db = self.mongo_client[database_name]
        self.bot.db = self.db

    def cog_unload(self):
        if hasattr(self.bot, "db"):
            del self.bot.db

        self.mongo_client.close()


def setup(bot):
    bot.add_cog(DatabaseService(bot, **bot.config.mongodb_options))
