import logging

from bot import Bot
from services.mongodb import MongoDBService

logging.basicConfig(
    filename="logs.log",
    level=logging.ERROR,
    format=r"%(levelname)s: %(message)s - %(asctime)s"
)

cogs = [
    "cogs.error_handler",
    "cogs.debug"
]

bot = Bot()
bot.load_cogs(cogs)
bot.add_service(MongoDBService)
bot.run()
