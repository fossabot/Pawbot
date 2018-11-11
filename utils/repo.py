from utils import default

version = "v1.3.0"
invite = "https://discord.gg/s4bSSCG"
owners = default.get("config.json").owners
contributors = default.get("config.json").contributors


def is_owner(ctx):
    return ctx.author.id in owners


def is_contributor(ctx):
    return ctx.author.id in contributors
