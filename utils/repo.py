from utils import default

version = "v1.3.0"
invite = "https://discord.gg/s4bSSCG"
owners = default.get("config.json").owners
contributors = default.get("config.json").contributors


def is_owner(ctx):
    return ctx.author.id in owners


def is_contributor(ctx):
    return ctx.author.id in contributors


def has_userID(ctx, userID):
    return ctx.author.id in userID


def has_guildID(ctx, guildID):
    return ctx.guild.id in guildID


def has_channelID(ctx, channelID):
    return ctx.channel.id in channelID