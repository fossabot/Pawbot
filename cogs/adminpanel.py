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
        query = "SELECT * FROM adminpanel WHERE serverid = $1;"
        row = await self.bot.db.fetchrow(query, ctx.guild.id)
        if row is None:
            query = "INSERT INTO adminpanel VALUES ($1, $2, $3, $4, $5, $6);"
            await self.bot.db.execute(query, ctx.guild.id, 1, 0, 0, 0, 1)
            query = "SELECT * FROM adminpanel WHERE serverid = $1;"
            row = await self.bot.db.fetchrow(query, ctx.guild.id)
        if row['embeds'] is 1:
            embedscheck = "<:enabled:513831607355047964>"
        else:
            embedscheck = "<:disabled:513831606855794709>"
        if row['joins'] is 1:
            joinleavecheck = "<:enabled:513831607355047964>"
        else:
            joinleavecheck = "<:disabled:513831606855794709>"
        if row['nsfw'] is 1:
            nsfwcheck = "<:enabled:513831607355047964>"
        else:
            nsfwcheck = "<:disabled:513831606855794709>"
        if row['automod'] is 1:
            automodcheck = "<:enabled:513831607355047964>"
        else:
            automodcheck = "<:disabled:513831606855794709>"
        if row['modlog'] is 1:
            modlogcheck = "<:enabled:513831607355047964>"
        else:
            modlogcheck = "<:disabled:513831606855794709>"
        embed = discord.Embed(colour=discord.Colour(0xdee05a))
        embed.add_field(name="Embeds", value=embedscheck, inline=True)
        embed.add_field(name="Join/Leave", value=joinleavecheck, inline=True)
        embed.add_field(name="NSFW", value=nsfwcheck, inline=True)
        embed.add_field(name="Automod", value=automodcheck, inline=True)
        embed.add_field(name="Modlog", value=modlogcheck, inline=True)
        embed.add_field(name="Experements", value="<:shh:513833978298368000>", inline=True)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(AdminPanel(bot))

# <:enabled:513831607355047964> <:disabled:513831606855794709>
# Embedding Joinleave NSFW
# Automod modlog experements
