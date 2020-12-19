import logging

from .bot import Bot
from .services.mongodb import MongoDBService

logging.basicConfig(
    filename="logs.log",
    level=logging.ERROR,
    format=r"%(levelname)s: %(message)s - %(asctime)s"
)

cogs = [
    "src.cogs.error_handler",
    "src.cogs.debug",
    "src.cogs.test"
]

bot = Bot()
bot.add_service(MongoDBService)
bot.load_cogs(cogs)
bot.run()
