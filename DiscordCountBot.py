import asyncio
import logging

from discord.ext import commands
from num2words import num2words

from utils import int_arg


logger = logging.getLogger('discord')
discordCountBot = commands.Bot(command_prefix='!')


@discordCountBot.command(name="count", help="Count to given number")
@int_arg
async def count(ctx: commands.context.Context, countdown: int):
    logger.info(f"{ctx.author}: {countdown}")

    for i in range(countdown):
        await asyncio.sleep(1)
        message = num2words(i + 1)
        await ctx.send(message)
        logger.info(f"counting to {countdown} for {ctx.author}: {message}")

    logger.info(f"countdoun to {countdown} for {ctx.author} finished")


@count.error
async def error_handler(ctx, error):
    await ctx.send(error)
    logger.info(f"answering to {ctx.author}: {error}")
    return
