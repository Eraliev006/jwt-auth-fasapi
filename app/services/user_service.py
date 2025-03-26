from logging import getLogger
from typing import Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.models import User
from logging_config import setup_logging
from app.schemas import CreateUserSchema, OutputUserSchema

setup_logging()
user_service_logger = getLogger('project.user_service')



async def get_user_by_email(email: str, session: AsyncSession) -> Optional[User]:
    try:
        user_service_logger.info("Getting user by email")

        stmt = select(User).where(User.email == email)

        user_service_logger.info("Make query to db, try to find user by email")
        result: Optional[User] = await session.scalar(stmt)

        user_service_logger.info("Return User instance or None after query")
        return result
    
    except SQLAlchemyError:
        user_service_logger.exception("Some problem with db: ")
        raise

async def create_user(session: AsyncSession, user: User) -> OutputUserSchema:

    try:
        user_service_logger.info('save user to db')
        user_service_logger.debug(user)
        user = User(**user.model_dump())

        session.add(user)
        await session.commit()
        await session.refresh(user)

        user_service_logger.info('commit query to db, user successfully created')

        return OutputUserSchema(**user.model_dump())

    except SQLAlchemyError:
        user_service_logger.exception('Some problem with DB')
        await session.rollback()

        user_service_logger.info(f'Session rollback')
        raise