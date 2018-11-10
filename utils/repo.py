from utils import default

version = "v1.3.0"
invite = "https://discord.gg/s4bSSCG"
owners = default.get("config.json").owners


def is_owner(ctx):
    return ctx.author.id in owners
