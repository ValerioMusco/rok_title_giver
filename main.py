#!/bin/bash

import config
from discord_bot.bot import Bot

with open("config/key.cfg", "r") as key_file:
    TOKEN = key_file.readline()

bot: Bot = Bot(config.COMMAND_PREFIX)

@bot.bot.command("title")
async def title(ctx, *args):
    # await ctx.send(args)
    await bot.title(ctx, args)

@bot.bot.command("done")
async def done(ctx):
    await bot.done(ctx)

bot.run(TOKEN)
