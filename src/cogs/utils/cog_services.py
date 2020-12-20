from discord.ext import commands


class ServiceCogMeta(commands.CogMeta):

    def __new__(cls, *args, **kwargs):
        required_services = kwargs.pop("required_services", [])
        new_cls = super().__new__(cls, *args, **kwargs)
        new_cls.required_services = required_services
        return new_cls


class ServiceCog(commands.Cog, metaclass=ServiceCogMeta):

    def __init__(self, bot):
        bot_cog_types = [type(cog) for cog in bot.cogs.values()]

        for service_type in self.required_services:
            if not any(issubclass(cog_type, service_type) for cog_type in bot_cog_types):
                raise TypeError(f"This cog requires {service_type.__qualname__} to be loaded.")

        self.bot = bot
