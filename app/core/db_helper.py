from collections.abc import AsyncGenerator
from logging import getLogger

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker, AsyncSession

from app.core import settings
import app.logger

db_helper_logger = getLogger('project.database_helper')


class DatabaseHelper:
    def __init__(
            self,
            url: str,
            pool_size: int = 5,
            echo: bool = True,
            max_overflow: int = 10,
            echo_pool: bool = False

    ):
        db_helper_logger.info('Create async engine')
        self.engine: AsyncEngine = create_async_engine(
            url = url,
            pool_size = pool_size,
            echo = echo,
            max_overflow = max_overflow,
            echo_pool = echo_pool
        )

        db_helper_logger.info('create async session')
        self.session_factory: async_sessionmaker[AsyncSession] =async_sessionmaker(
            bind = self.engine,
            expire_on_commit = False,
            autoflush = False,
            autocommit = False
        )

    async def dispose(self):
        db_helper_logger.info('Dispose connection with db')
        return await self.engine.dispose()

    @property
    async def session_getter(self) -> AsyncGenerator[AsyncSession]:
        async with self.session_factory as session:
            db_helper_logger.info('returning session')
            yield session

db_helper = DatabaseHelper(settings.db.db_url,echo_pool=True)
