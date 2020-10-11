from pymongo import MongoClient
from cogs.utils.service import BotService


class MongoDBService(BotService):

    def __init__(self, *args):
        super().__init__(*args)
        self.mongo_client = MongoClient(
            self.bot.config.mongodb_host,
            self.bot.config.mongodb_port
        )
        self.db = self.mongo_client[self.bot.config.mongodb_name]

