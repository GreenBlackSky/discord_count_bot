"""Module conatins the core bot logic."""

import asyncio
from datetime import datetime, timedelta
import logging
import re
import traceback

import discord
from num2words import num2words

from db_hanler import dbConnection, TaskModel


logger = logging.getLogger('discord')
COUNT_TEMPLATE = r"^(<@\![0-9]{18}> )?count to [0-9]{1,4}$"
STOP_TEMPLATE = r"^(<@\![0-9]{18}> )?stop"


class CountBot(discord.Client):
    """This class contains all the bot high-level logic."""

    def __init__(self, *, loop=None, **options):
        """Create new bot."""
        super().__init__(loop=loop, **options)
        self._active_tasks = {}

    async def on_ready(self):
        """Resume active tasks."""
        for (task,) in await dbConnection.get_active_tasks():
            logger.info(f"continuing task {task}")
            self._active_tasks[task.channel_id] = asyncio.create_task(
                self.start_counting(task)
            )

    async def on_message(self, message: discord.Message):
        """
        React to user message.

        Parse message and if it is a command, process it.
        """
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

        channel_id = message.author.id if is_dm else message.channel.id
        if re.fullmatch(COUNT_TEMPLATE, message.content):
            await self.process_start_command(message, channel_id, is_dm)
        elif re.fullmatch(STOP_TEMPLATE, message.content):
            await self.process_stop_command(message, channel_id)
        else:
            await self.not_a_command(message)

    async def process_start_command(
        self, message: discord.Message, channel_id, is_dm
    ):
        """Start countdown in channel if it is not alredy on."""
        if channel_id in self._active_tasks:
            await message.channel.send("I am already counting here.")
            await message.channel.send("Either send command to another chat or stop countdown here.")
            logger.info(f"{message.author} attempted to start second countdown in {channel_id}")
            return

        task = await dbConnection.add_task(
            author=message.author,
            channel_id=channel_id,
            count=int(message.content.split()[-1]),
            is_dm=is_dm,
            time=message.created_at
        )
        logger.info(f"start task: {task}")
        self._active_tasks[task.channel_id] = asyncio.create_task(
            self.start_counting(task)
        )

    async def process_stop_command(self, message: discord.Message, channel_id):
        """Stop countdown if there is one."""
        if channel_id not in self._active_tasks:
            await message.channel.send("I am not currently counting in this chat.")
            logger.info(f"{message.author} attempted to stop non-existant countdown in {message.channel.id}")
            return

        self._active_tasks[channel_id].cancel()
        del self._active_tasks[channel_id]
        await dbConnection.cancel_task(channel_id)
        await message.channel.send("Countdown stopped.")

    async def not_a_command(self, message: discord.Message):
        """Notify user that his command is not a command."""
        reply = f"{message.content} is not a command"
        await message.channel.send(reply)
        logger.info(reply)

    async def start_counting(self, task: TaskModel):
        """Send user number each second."""
        if task.is_dm:
            channel = await self.fetch_user(task.channel_id)
        else:
            channel = self.get_channel(task.channel_id)

        now = datetime.utcnow()
        start = task.start_time
        delta = now - start
        next_time = start + delta
        for i in range(int(delta.total_seconds()), task.count):
            asyncio.create_task(channel.send(num2words(i + 1)))
            # dynamic sleep period somehow makes it worse 0_o
            sleep_for = 1
            # now = datetime.utcnow()
            # next_time += timedelta(seconds=1)
            # sleep_for = (next_time - now).total_seconds()
            # if sleep_for < 0.5:
            #     continue
            await asyncio.sleep(sleep_for)

        await channel.send("Countdown finished.")
        del self._active_tasks[task.channel_id]
        logger.info(f"task finished :{task}")

    async def on_error(self, event_method, *args, **kwargs):
        """Save error log in db."""
        trace = traceback.format_exc()
        if event_method == "on_message":
            await dbConnection.log_command_error(args[0], trace)
            logger.error(f'Command error: {args[0]} : {trace}')
        else:
            await dbConnection.log_general_error(event_method, f"{args}, {kwargs}", trace)
            logger.error(f'Unknown error: {event_method}, {args}, {kwargs}, {trace}')
