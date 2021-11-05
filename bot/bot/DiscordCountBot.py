import asyncio
from datetime import datetime
import logging
import re

import discord
from num2words import num2words

from db_hanler import dbConnection, TaskModel


logger = logging.getLogger('discord')
TEMPLATE = r"^(<@\![0-9]{18}> )?count to [0-9]{1,4}$"


class CountBot(discord.Client):
    async def on_ready(self):
        dbConnection.clearExpiredTasks()
        for task in dbConnection.getTasks():
            logger.info(f"continuing counting for {task.author} in {task.channel_id}")
            asyncio.create_task(self.start_counting(task))

    async def on_message(self, message: discord.Message):
        if message.author == self.user:
            return
        is_dm = False
        if isinstance(message.channel, discord.channel.DMChannel):
            is_dm = True
            logger.info(f"{message.author} in DM: {message.content}")
        elif self.user in message.mentions:
            logger.info(f"{message.author} tagged bot: {message.content}")
        else:
            return

        if re.fullmatch(TEMPLATE, message.content) is None:
            logger.info(f"{message.content} is not a command")
            return

        task = dbConnection.addTask(
            author=str(message.author),
            channel_id=message.author.id if is_dm else message.channel.id,
            count=int(message.content.split()[-1]),
            is_dm=is_dm
        )
        logger.info(f"start counting for {task.author} in {task.channel_id}")
        asyncio.create_task(self.start_counting(task))

    async def start_counting(self, task: TaskModel):
        if task.is_dm:
            channel = await self.fetch_user(task.channel_id)
        else:
            channel = self.get_channel(task.channel_id)

        count_start = int((datetime.utcnow() - task.start_time).total_seconds())
        for i in range(count_start, task.count):
            await channel.send(num2words(i + 1))
            await asyncio.sleep(1)

        logger.info(f"finished counting to {task.count} for {task.author} in {task.channel_id}")
        dbConnection.removeTask(task)
