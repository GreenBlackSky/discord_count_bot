import asyncio
import logging
import re
import datetime

import discord
from num2words import num2words

from db_hanler import dbConnection


logger = logging.getLogger('discord')
TEMPLATE = r"^(<@\![0-9]{18}> )?count to [0-9]{4}$"


class CountBot(discord.Client):
    async def on_message(self, message: discord.Message):
        if message.author == self.user:
            return
        if isinstance(message.channel, discord.channel.DMChannel):
            logger.info(f"{message.author} in DM: {message.content}")
        elif self.user in message.mentions:
            logger.info(f"{message.author} tagged bot: {message.content}")
        else:
            return

        if re.fullmatch(TEMPLATE, message.content) is None:
            logger.info(f"{message.content} is not a command")
            return

        countdown = int(message.content.split()[-1])
        Model = dbConnection.getCountdownModel()
        countdownDB = Model(
            chanell_id=message.channel.id,
            start_time=datetime.datetime.now(),
            countdown=int(message.content.split()[-1])
        )
        dbConnection.session.add(countdownDB)
        dbConnection.session.commit()

        for i in range(countdown):
            await asyncio.sleep(1)
            reply = num2words(i + 1)
            await message.channel.send(reply)
            logger.info(
                f"counting to {countdown} for {message.author}: {reply}"
            )

        logger.info(f"countdoun to {countdown} for {message.author} finished")
