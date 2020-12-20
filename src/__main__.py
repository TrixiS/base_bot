import logging

from .bot import Bot

logging.basicConfig(
    filename="logs.log",
    level=logging.ERROR,
    format=r"%(levelname)s: %(message)s - %(asctime)s"
)

cogs = [
    "src.cogs.database_service",
    "src.cogs.language_service",
    "src.cogs.error_handler",
    "src.cogs.debug",
    "src.cogs.test"
]

bot = Bot()
bot.load_cogs(cogs)
bot.run()
