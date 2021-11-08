"""Main entry point for bot."""

import os

from logger import init_logging
from db_hanler import dbConnection
from DiscordCountBot import client
from prometheus_handler import prometheus, quart


init_logging()

dbConnection.init_connection(
    os.environ['POSTGRES_USER'],
    os.environ['POSTGRES_PASSWORD'],
    os.environ['POSTGRES_HOST'],
    os.environ['POSTGRES_PORT'],
    os.environ['POSTGRES_DB']
)

prometheus.init()

client.loop.create_task(quart.run_task(host='0.0.0.0'))
client.run(os.getenv('DISCORD_TOKEN'))
