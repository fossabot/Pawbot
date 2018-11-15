import discord

from discord.ext import commands
from utils import permissions, default


class AdminPanel:
    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("config.json")

    @commands.command()
    @commands.guild_only()
    @permissions.has_permissions(Admininstartor=True)
    async def adminpanel(self, ctx):
        embed = discord.Embed(title="This embed is a test", colour=discord.Colour(0xdee05a))
        embed.add_field(name="This", value="hhh", inline=True)
        embed.add_field(name="Is", value="hhh", inline=True)
        embed.add_field(name="​", value="​", inline=True)
        embed.add_field(name="This", value="hhh", inline=True)
        embed.add_field(name="Is", value="hhh", inline=True)
        embed.add_field(name="​", value="​", inline=True)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(AdminPanel(bot))
