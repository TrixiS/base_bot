from motor.motor_asyncio import AsyncIOMotorClient

from .service import BotService


class MongoDBService(BotService):

    def __init__(self, *args):
        super().__init__(*args)
        self.mongo_client = AsyncIOMotorClient(
            self.bot.config.mongodb_host,
            self.bot.config.mongodb_port
        )
        self.db = self.mongo_client[self.bot.config.mongodb_name]
        self.bot.db = self.db

    async def close(self):
        self.mongo_client.close()
