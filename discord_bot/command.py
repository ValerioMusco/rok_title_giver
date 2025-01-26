import config
from custom_types import Title, Kingdom

import discord
from discord.ext import commands

from queue import Queue


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=config.COMMAND_PREFIX, intents=intents)

# Command should look like this : /title XXX {HOME|LOST} X Y
@bot.command()
async def title(ctx, *args):
    if len(args) != 4:
        return

    # Parse the command args into individual variable
    try:
        title: str = Title.__getitem__(args[0]).value
    except KeyError:
        ctx.send(f"{args[0]} wasn't recognised as a title.")
        return

    try:
        kingdom: str = Kingdom.__getitem__(args[1]).value
    except KeyError:
        ctx.send(f"Kingdom {args[1]} wasn't recognised")
        return

    try:
        coord_x: int = int(args[2])
    except ValueError:
        ctx.send(f"{args[2]} isn't a valid X coordinate value.")
        return

    try:
        coord_y: int = int(args[3])
    except ValueError:
        ctx.send(f"{args[3]} isn't a valid Y coordinate value.")
        return





bot.add_command(title)
