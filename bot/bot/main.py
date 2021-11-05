"""Main entry point for bot."""

import os

from logger import init_logging
from db_hanler import dbConnection
from DiscordCountBot import CountBot


init_logging()
dbConnection.init_connection(
    os.environ['POSTGRES_USER'],
    os.environ['POSTGRES_PASSWORD'],
    os.environ['POSTGRES_HOST'],
    os.environ['POSTGRES_PORT'],
    os.environ['POSTGRES_DB']
)
CountBot().run(os.getenv('DISCORD_TOKEN'))
