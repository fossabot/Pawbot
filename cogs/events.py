import discord
import traceback
import psutil
import os

from discord_webhook import DiscordWebhook, DiscordEmbed
from datetime import datetime
from discord.ext.commands import errors
from utils import default


async def send_cmd_help(ctx):
    if ctx.invoked_subcommand:
        _help = await ctx.bot.formatter.format_help_for(ctx, ctx.invoked_subcommand)
    else:
        _help = await ctx.bot.formatter.format_help_for(ctx, ctx.command)

    for page in _help:
        await ctx.send(page)


class Events:
    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("config.json")
        self.process = psutil.Process(os.getpid())

    async def on_command_error(self, ctx, err):
        if isinstance(err, errors.MissingRequiredArgument) or isinstance(err, errors.BadArgument):
            await send_cmd_help(ctx)

        elif isinstance(err, errors.CommandInvokeError):
            err = err.original

            _traceback = traceback.format_tb(err.__traceback__)
            _traceback = ''.join(_traceback)
            error = '```py\n{2}{0}: {3}\n```'.format(type(err).__name__, ctx.message.content, _traceback, err)
            logchannel = self.bot.get_channel(508420200815656966)
            await ctx.send("There was an error in processing the command, our staff have been notified.")
            await logchannel.send(f"`ERROR`\n{error}\nRoot server: {ctx.guild.name} ({ctx.guild.id})\nRoot user: {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})")

        elif isinstance(err, errors.CheckFailure):
            pass

        elif isinstance(err, errors.CommandOnCooldown):
            await ctx.send(f"This command is on cooldown... try again in {err.retry_after:.0f} seconds.")

        elif isinstance(err, errors.CommandNotFound):
            pass

    async def on_ready(self):
        if not hasattr(self.bot, 'uptime'):
            self.bot.uptime = datetime.utcnow()
        webhook = DiscordWebhook(url=f'{self.config.welcomewebhook}')
        embed = DiscordEmbed(title=f'Reconnected, Online and Operational!', description='Ready Info', color=5810826)
        embed.set_author(name=f'PawBot', url='https://discordapp.com/oauth2/authorize?client_id=460383314973556756&scope=bot&permissions=469888118', icon_url='https://cdn.discordapp.com/avatars/460383314973556756/d96ff7682f89483c4864f7af4b3a096c.png?size=2048')
        embed.add_embed_field(name='Stats', value=f'Guilds:** {len(self.bot.guilds)}**\nUsers:** {len(self.bot.users)}**\n\o/')
        embed.set_timestamp()
        webhook.add_embed(embed)
        await self.bot.change_presence(activity=discord.Game(type=0, name=self.config.playing), status=discord.Status.online)
        webhook.execute()


def setup(bot):
    bot.add_cog(Events(bot))
