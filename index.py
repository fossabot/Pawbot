#Pybot by Paws#0001

import discord
import random

from discord.ext import commands
from discord.ext.commands import Bot
import asyncio

bot = commands.Bot(command_prefix='!')

bot.remove_command("help")

@bot.event
async def on_ready():
    print ("I'm ready!")
    await bot.change_presence(game=discord.Game(name='!commands for commands'))

@bot.command(pass_context=True)
async def ping(ctf):
    await bot.say(":ping_pong: Pong!")

@bot.command(pass_context=True)
async def serverinfo(ctx):
    embed = discord.Embed(name="{}'s info".format(ctx.message.server.name), description="Here's what I could find.", color=0x00ff00)
    embed.set_author(name="Server information!")
    embed.add_field(name="Name", value=ctx.message.server.name, inline=True)
    embed.add_field(name="ID", value=ctx.message.server.id, inline=True)
    embed.add_field(name="Roles", value=len(ctx.message.server.roles), inline=True)
    embed.add_field(name="Members", value=len(ctx.message.server.members))
    embed.set_thumbnail(url=ctx.message.server.icon_url)
    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def botsize(ctx):
    await bot.say('I am in {} servers'.format(len(bot.servers)))

@bot.command(pass_context=True)
async def echo(ctx, arg):
    await bot.say(arg)

@bot.command(pass_context=True)
async def help(ctx):
    await bot.say("```\nMy commands are:\n  !help\n  !echo\n  !ping\n  !serverinfo\n  !botsize\n```")

@bot.command(pass_context=True)
async def test(ctx):
    author = ctx.message.author
    await bot.say("Your username is: {}, your ID is: {}, your nickname is: {}".format(author.name, author.id, author.nick))

bot.run("YOUR TOKEN HERE")
