import random
import discord
import json
import requests
import io

from io import BytesIO
from discord.ext import commands
from utils import lists, permissions, http, default
from utils.lists import *


class NSFW_Commands:
    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("config.json")

    async def randomimageapi(self, ctx, url, endpoint):
        try:
            r = await http.get(url, res_method="json", no_cache=True)
        except json.JSONDecodeError:
            return await ctx.send("Couldn't find anything from the API")

        embed = discord.Embed(colour=0xff50e0)
        embed.set_image(url=r[endpoint])
        await ctx.send(embed=embed)



    @commands.command()
    @commands.is_nsfw()
    @commands.cooldown(rate=1, per=5.0, type=commands.BucketType.user)
    async def lewdneko(self, ctx):
        """ Posts a lewd neko """
        await self.randomimageapi(ctx, 'https://nekos.life/api/v2/img/lewd', 'url')

    @commands.command()
    @commands.is_nsfw()
    @commands.cooldown(rate=1, per=5.0, type=commands.BucketType.user)
    async def lewdfeet(self, ctx):
        """ Posts a lewd foot image or gif """
        randomfoot = ["feet", "feetg"]
        await self.randomimageapi(ctx, f'https://nekos.life/api/v2/img/{random.choice(randomfoot)}', 'url')

    @commands.command()
    @commands.is_nsfw()
    @commands.cooldown(rate=1, per=5.0, type=commands.BucketType.user)
    async def lewdkemo(self, ctx):
        """ Posts a lewd kemonomimi character """
        randomfox = ["holoero", "erokemo", "hololewd"]
        await self.randomimageapi(ctx, f'https://nekos.life/api/v2/img/{random.choice(randomfox)}', 'url')

    @commands.command()
    @commands.is_nsfw()
    @commands.cooldown(rate=1, per=5.0, type=commands.BucketType.user)
    async def lewdanal(self, ctx):
        """ Posts a lewd anal gif/picture """
        await self.randomimageapi(ctx, f'https://nekos.life/api/v2/img/anal', 'url')


def setup(bot):
    bot.add_cog(NSFW_Commands(bot))
