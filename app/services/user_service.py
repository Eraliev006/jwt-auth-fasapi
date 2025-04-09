from logging import getLogger
from typing import Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.exceptions import UserWithIdNotFound, UserWithEmailNotFound
from app.models import User
from logging_config import setup_logging

setup_logging()
user_service_logger = getLogger('project.user_service')



async def get_user_by_email(email: str, session: AsyncSession) -> Optional[User]:
    user_service_logger.info("Getting user by email")
    try:

        stmt = select(User).where(User.email == email)

        user_service_logger.info("Make query to db, try to find user by email")
        user: Optional[User] = await session.scalar(stmt)

    except SQLAlchemyError:
        user_service_logger.exception("Some problem with db: ")
        raise

    if not user:
        raise UserWithEmailNotFound

    user_service_logger.info("Return User by email")
    return user



async def create_user(session: AsyncSession, user: User) -> User:
    user_service_logger.info('save user to db')
    try:
        user = User(**user.model_dump())

        session.add(user)
        await session.commit()
        await session.refresh(user)

    except SQLAlchemyError:
        user_service_logger.exception('Some problem with DB')
        await session.rollback()

        user_service_logger.info(f'Session rollback')
        raise

    user_service_logger.info('commit query to db, user successfully created')
    return user



async def get_user_by_id(user_id:int, session: AsyncSession) -> User:
    user_service_logger.info('Getting a user by id')
    try:
        user: Optional[User] = await session.get(User, user_id)
    except SQLAlchemyError as e:
        user_service_logger.exception('Exception with db:')
        raise e

    if user is None:
        user_service_logger.error('User with ID not found')
        raise UserWithIdNotFound

    user_service_logger.info('Returning user by id')
    return user

async def change_user_verify_status(user: User, session: AsyncSession):
    user_service_logger.info('Change user is_verify status')
    try:
        user.is_verified = True
        user_service_logger.info('user is_verify status changed')
        await session.commit()
    except SQLAlchemyError as e:
        user_service_logger.exception('Exception with db:')
        raise e
