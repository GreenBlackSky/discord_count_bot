import os
import sys
import logging

from dotenv import load_dotenv

from DiscordCountBot import discordCountBot


fileHandler = logging.FileHandler(
    filename='discord.log',
    encoding='utf-8',
    mode='w'
)
consoleHandler = logging.StreamHandler(sys.stdout)

formatter = logging.Formatter(
    "%(asctime)s:%(levelname)s:%(name)s: %(message)s"
)
fileHandler.setFormatter(formatter)
consoleHandler.setFormatter(formatter)

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
logger.addHandler(fileHandler)
logger.addHandler(consoleHandler)


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


discordCountBot.run(TOKEN)
