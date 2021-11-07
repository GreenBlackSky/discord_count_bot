"""Database-level logic."""

from datetime import datetime, timedelta
import logging
import discord

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, update, and_
from sqlalchemy import Column, Integer, String, DateTime, Boolean, BigInteger

logger = logging.getLogger('discord')
Base = declarative_base()


class TaskModel(Base):
    """Counting task model for database."""

    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    author_name = Column(String(200))
    author_id = Column(BigInteger)
    channel_id = Column(BigInteger)
    is_dm = Column(Boolean)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    count = Column(Integer)
    canceled = Column(Boolean)

    def __repr__(self):
        """Print task."""
        return f"<Counting task id: {self.id}, \
author name: {self.author_name}, author id: {self.author_id}, \
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
    author_id = Column(BigInteger)
    channel_id = Column(BigInteger)
    is_dm = Column(Boolean)
    time = Column(DateTime)
    traceback = Column(String(2000))


class DBConnection:
    """Class handles all the db operations."""

    def __init__(self):
        """Create new uninitialized handler."""
        self._session: AsyncSession = None

    def init_connection(self, user, password, host, port, db):
        """Connect to actual database."""
        connection_string = "postgresql+asyncpg://{}:{}@{}:{}/{}".format(
            user, password, host, port, db
        )
        engine = create_async_engine(connection_string, future=True, echo=True)
        self._session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    async def add_task(self, author: discord.Member, channel_id, count, is_dm):
        """Add new task to db."""
        now = datetime.utcnow()
        async with self._session() as session:
            task = TaskModel(
                author_name=author.display_name[:200],
                author_id=author.id,
                channel_id=channel_id,
                is_dm=is_dm,
                start_time=now,
                end_time=now + timedelta(seconds=count),
                count=count,
                canceled=False
            )
            session.add(task)
            await session.commit()
            logger.info(f"task added to db: {task}")
            return task

    async def get_active_tasks(self):
        """Get all active tasks."""
        now = datetime.utcnow()
        async with self._session() as session:
            query = select(TaskModel).where(and_(
                    TaskModel.end_time > now,
                    TaskModel.canceled == False
            ))
            result = await session.execute(query)
            return result

    async def cancel_task(self, channel_id):
        """Cancel active task in given channel."""
        now = datetime.utcnow()
        async with self._session() as session:
            query = update(TaskModel)\
                .where(and_(
                    TaskModel.channel_id == channel_id,
                    TaskModel.end_time > now,
                    TaskModel.canceled == False))\
                .values(canceled=True)
            await session.execute(query)
            await session.commit()
        logger.info(f"task canceled")

    async def log_general_error(self, method, error_info, trace):
        """Log general error into db."""
        async with self._session() as session:
            error = GeneralErrorModel(
                time=datetime.utcnow(),
                method=method[:200],
                error_info=error_info[:2000],
                traceback=trace[:2000]
            )
            session.add(error)
            await session.commit()

    async def log_command_error(self, message: discord.Message, trace):
        """Log command error."""
        is_dm = isinstance(message.channel, discord.channel.DMChannel)
        channel_id = message.author.id if is_dm else message.channel.id
        async with self._session() as session:
            error = CommandErrorModel(
                command=message.content[:200],
                author_name=message.author.display_name[:200],
                author_id=message.author.id,
                channel_id=channel_id,
                is_dm=is_dm,
                time=datetime.utcnow(),
                traceback=trace[:2000]
            )
            session.add(error)
            await session.commit()


dbConnection = DBConnection()
