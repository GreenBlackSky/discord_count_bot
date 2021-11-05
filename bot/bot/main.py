import os

from logger import init_logging
from db_hanler import dbConnection
from DiscordCountBot import CountBot


init_logging()
dbConnection.init_connection()
CountBot().run(os.getenv('DISCORD_TOKEN'))
