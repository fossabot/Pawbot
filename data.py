from utils import permissions, default

config = default.get("config.json")

from discord.ext.commands import AutoShardedBot

class Bot(AutoShardedBot):
    def __init__(self, *args, prefix=None, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_message(self, msg):
        if not self.is_ready() or msg.author.bot or not permissions.can_send(msg):
            return

        if msg.guild.id in config.serverblacklist:
            return
        elif msg.author.id in config.userblacklist:
            return

        #This logs any commands, no other messages are logged.
        if any(c in msg.content for c in config.prefix):
            commandlog = self.get_channel(448947806196203520)
            await commandlog.send(f"`{msg.author.name}#{msg.author.discriminator}` `({msg.author.id})`, `{msg.guild.name}` (`{msg.guild.id}`): `{msg.content}`")
        else:
            pass

        if msg.channel.id == config.uplinkchannel:
            connectionchannel = self.get_channel(config.downlink)

            await connectionchannel.send(f'{msg.author.name}#{msg.author.discriminator}: {msg.content}')

        if msg.channel.id == config.downlink:
            connectionchannel1 = self.get_channel(config.uplinkchannel)

            await connectionchannel1.send(f'{msg.author.name}#{msg.author.discriminator}: {msg.content}')

        await self.process_commands(msg)
