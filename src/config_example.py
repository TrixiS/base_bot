from discord import Intents

bot_token: str = ""
command_prefixes: list = ["!", "!!"]

discord_intents: Intents = Intents.all()

mongodb_options: dict = {
    "host": "localhost",
    "port": 27017,
    "database_name": "discord_bot"
}
