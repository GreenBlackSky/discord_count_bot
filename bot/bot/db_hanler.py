import os
from datetime import datetime, timedelta
import logging

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, Boolean

logger = logging.getLogger('discord')


class TaskModel(declarative_base()):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    author = Column(String(200))
    channel_id = Column(Integer)
    is_dm = Column(Boolean)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    count = Column(Integer)

    def __repr__(self):
        return f"<id: {self.id}, author: {self.author}, \
channel_id: {self.channel_id}, is_dm: {self.is_dm}, \
start_time: {self.start_time}, end_time: {self.end_time}, count: {self.count}>"


class DBConnection:
    def __init__(self):
        self._session: Session = None

    def init_connection(self):
        connection_string = "postgresql://{}:{}@{}:{}/{}".format(
            os.environ['POSTGRES_USER'],
            os.environ['POSTGRES_PASSWORD'],
            os.environ['POSTGRES_HOST'],
            os.environ['POSTGRES_PORT'],
            os.environ['POSTGRES_DB'],
        )
        engine = create_engine(connection_string)
        self._session = Session(engine)

    def addTask(self, author, channel_id, count, is_dm):
        now = datetime.utcnow()
        task = TaskModel(
            author=author,
            channel_id=channel_id,
            is_dm=is_dm,
            start_time=now,
            end_time=now + timedelta(seconds=count),
            count=count
        )
        self._session.add(task)
        self._session.commit()
        logger.info(f"task added to db: {task}")
        return task

    def getTasks(self):
        return self._session.query(TaskModel).all()

    def clearExpiredTasks(self):
        now = datetime.utcnow()
        query = self._session.query(TaskModel).filter(TaskModel.end_time <= now)
        tasks = query.all()
        query.delete()
        self._session.commit()
        for task in tasks:
            logger.info(f"task removed due to exparation: {task}")

    def removeTask(self, task: TaskModel):
        self._session.delete(task)
        self._session.commit()
        logger.info(f"task removed: {task}")


dbConnection = DBConnection()
