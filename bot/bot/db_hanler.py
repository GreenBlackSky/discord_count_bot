import os

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine


class DBConnection:
    def __init__(self):
        self._countdownModel = None
        self._session: Session = None

    def init_connection(self):
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

        self._countdownModel = Base.classes.countdowns
        self._session = Session(engine)

    def getCountdownModel(self):
        return self._countdownModel

    @property
    def session(self):
        return self._session


dbConnection = DBConnection()
