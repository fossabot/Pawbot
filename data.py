from utils import permissions, default

config = default.get("config.json")

from discord.ext.commands import AutoShardedBot

class Bot(AutoShardedBot):
    def __init__(self, *args, prefix=None, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_message(self, msg):
        if not self.is_ready() or msg.author.bot or not permissions.can_send(msg):
            return

        if msg.channel.id == config.uplinkchannel:
            connectionchannel = self.get_channel(config.downlink)

            await connectionchannel.send(f'{msg.author.name}#{msg.author.discriminator}: {msg.content}')

        if msg.channel.id == config.downlink:
            connectionchannel1 = self.get_channel(config.uplinkchannel)

            await connectionchannel1.send(f'{msg.author.name}#{msg.author.discriminator}: {msg.content}')

        await self.process_commands(msg)
