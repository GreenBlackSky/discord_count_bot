import os
import sys
import logging

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from DiscordCountBot import CountBot


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


connection_string = "postgresql://{}:{}@{}:{}/{}".format(
    os.environ['POSTGRES_USER'],
    os.environ['POSTGRES_PASSWORD'],
    os.environ['POSTGRES_HOST'],
    os.environ['POSTGRES_PORT'],
    os.environ['POSTGRES_DB'],
)

Base = automap_base()
engine = create_engine(connection_string)
Base.prepare(engine, reflect=True)

UserModel = Base.classes.countdowns

session = Session(engine)


TOKEN = os.getenv('DISCORD_TOKEN')


CountBot().run(TOKEN)
