from utils import permissions, default
from discord.ext.commands import AutoShardedBot
import discord

config = default.get("config.json")


class Bot(AutoShardedBot):
    def __init__(self, *args, prefix=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = kwargs.pop("db")

    async def on_message(self, msg):
        if not self.is_ready() or msg.author.bot or not permissions.can_send(msg):
            return
        else:
            await self.process_commands(msg)
