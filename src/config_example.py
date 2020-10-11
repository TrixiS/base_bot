from discord import Intents

bot_token: str = ""
command_prefixes: list = ["!", "!!"]

discord_intents: Intents = Intents.all()

mongodb_host: str = "localhost"
mongodb_port: str = 27017
mongodb_name: str = "discord_bot"
