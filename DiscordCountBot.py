import asyncio
import logging

from discord.ext import commands
from num2words import num2words

logger = logging.getLogger('discord')
discordCountBot = commands.Bot(command_prefix='!')


@discordCountBot.command()
async def count(ctx: commands.context.Context, *args):
    logger.info(f"{ctx.author}: {args}")

    response = None
    if not args:
        response = "count till what?"
    elif len(args) > 1:
        response = f"can't count to {args}"
    countdown = args[0]
    if not countdown.isnumeric():
        response = f"can't count to {countdown}"

    if response:
        await ctx.send(response)
        logger.info(f"answering to {ctx.author}: {response}")
        return

    for i in range(int(countdown)):
        await asyncio.sleep(1)
        message = num2words(i + 1)
        await ctx.send(message)
        logger.info(f"counting to {countdown} for {ctx.author}: {message}")

    logger.info(f"countdoun to {countdown} for {ctx.author} finished")
