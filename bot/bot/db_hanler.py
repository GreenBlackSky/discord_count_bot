"""Database-level logic."""

from datetime import datetime, timedelta
import logging

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, Boolean

logger = logging.getLogger('discord')


class TaskModel(declarative_base()):
    """Counting task model for database."""

    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    author = Column(String(200))
    channel_id = Column(Integer)
    is_dm = Column(Boolean)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    count = Column(Integer)
    canceled = Column(Boolean)

    def __repr__(self):
        """Print task."""
        return f"<id: {self.id}, author: {self.author}, \
channel_id: {self.channel_id}, is_dm: {self.is_dm}, \
start_time: {self.start_time}, end_time: {self.end_time}, \
count: {self.count}, canceled: {self.canceled}>"


class DBConnection:
    """Class handles all the db operations."""

    def __init__(self):
        """Create new uninitialized handler."""
        self._session: Session = None

    def init_connection(self, user, password, host, port, db):
        """Connect to actual database."""
        connection_string = "postgresql://{}:{}@{}:{}/{}".format(
            user, password, host, port, db
        )
        engine = create_engine(connection_string)
        self._session = Session(engine)

    def add_task(self, author, channel_id, count, is_dm):
        """Add new task to db."""
        now = datetime.utcnow()
        task = TaskModel(
            author=author,
            channel_id=channel_id,
            is_dm=is_dm,
            start_time=now,
            end_time=now + timedelta(seconds=count),
            count=count,
            canceled=False
        )
        self._session.add(task)
        self._session.commit()
        logger.info(f"task added to db: {task}")
        return task

    def get_active_tasks(self):
        """Get all active tasks."""
        now = datetime.utcnow()
        return self._session\
            .query(TaskModel)\
            .filter(TaskModel.end_time > now)\
            .filter(TaskModel.canceled == False)\
            .all()

    def cancel_task(self, channel_id):
        """Cancel active task in given channel."""
        now = datetime.utcnow()
        task = self._session\
            .query(TaskModel)\
            .filter(TaskModel.channel_id == channel_id)\
            .filter(TaskModel.end_time > now)\
            .filter(TaskModel.canceled == False)\
            .first()
        if task is None:
            logger.info(f"can't cancel task in {channel_id}")
            return
        task.canceled = True
        self._session.commit()
        logger.info(f"task canceled: {task}")


dbConnection = DBConnection()
