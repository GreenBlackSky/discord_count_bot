import asyncio
import logging

from discord.ext import commands


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
        await ctx.send(i)
        logger.info(f"counting to {countdown} for {ctx.author}: {i}")

    logger.info(f"countdoun to {countdown} for {ctx.author} finished")
