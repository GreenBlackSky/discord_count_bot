"""Database-level logic."""

from datetime import datetime, timedelta
import logging
import discord

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, Boolean

logger = logging.getLogger('discord')
Base = declarative_base()


class TaskModel(Base):
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


class GeneralErrorModel(Base):
    """Any non-command error."""

    __tablename__ = 'general_errors'

    id = Column(Integer, primary_key=True)
    time = Column(DateTime)
    method = Column(String(200))
    error_info = Column(String(2000))
    traceback = Column(String(2000))


class CommandErrorModel(Base):
    """Error while processing command."""

    __tablename__ = 'command_errors'

    id = Column(Integer, primary_key=True)
    command = Column(String(200))
    author_name = Column(String(200))
    author_id = Column(Integer)
    channel_id = Column(Integer)
    is_dm = Column(Boolean)
    time = Column(DateTime)
    traceback = Column(String(2000))


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

    def log_general_error(self, method, error_info, trace, time):
        """Log general error into db."""
        error = GeneralErrorModel(
            time=datetime.utcnow(),
            method=method[:200],
            error_info=error_info[:2000],
            traceback=trace[:2000]
        )
        self._session.add(error)
        self._session.commit()

    def log_command_error(self, message: discord.Message, trace, time):
        """Log command error."""
        is_dm = isinstance(message.channel, discord.channel.DMChannel)
        channel_id = message.author.id if is_dm else message.channel.id
        error = CommandErrorModel(
            command=message.content[:200],
            author_name=message.author.display_name[:200],
            author_id=message.author.id,
            channel_id=channel_id,
            is_dm=is_dm,
            time=datetime.utcnow(),
            traceback=trace[:2000]
        )
        self._session.add(error)
        self._session.commit()


dbConnection = DBConnection()
