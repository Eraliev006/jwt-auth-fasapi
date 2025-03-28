from logging import getLogger
from typing import Optional

from sqlalchemy import Result
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.exceptions import UserWithIdNotFound
from app.models import User
from logging_config import setup_logging
from app.schemas import OutputUserSchema

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

async def create_user(session: AsyncSession, user: User) -> User:

    try:
        user_service_logger.info('save user to db')
        user_service_logger.debug(user)
        user = User(**user.model_dump())

        session.add(user)
        await session.commit()
        await session.refresh(user)

        user_service_logger.info('commit query to db, user successfully created')

        return user

    except SQLAlchemyError:
        user_service_logger.exception('Some problem with DB')
        await session.rollback()

        user_service_logger.info(f'Session rollback')
        raise

async def get_user_by_id(user_id:int, session: AsyncSession) -> User:
    try:
        user_service_logger.info('Getting a user by id')
        user: Optional[User] = await session.get(User, user_id)
        if user is None:
            user_service_logger.error('User with ID not found')
            raise UserWithIdNotFound(f'User with ID - {user_id} not found')

        user_service_logger.info('Returning user by id')
        return user

    except SQLAlchemyError as e:
        user_service_logger.exception('Exception with db:')
        raise e

async def change_user_verify_status(user: User, session: AsyncSession):
    try:
        user_service_logger.info('Change user is_verify status')
        user.is_verified = True
        user_service_logger.info('user is_verify status changed')
        await session.commit()
    except SQLAlchemyError as e:
        user_service_logger.exception('Exception with db:')
        raise e

async def delete_user(user_id: int, session: AsyncSession) -> None:
    try:
        user_service_logger.info('Try to delete user by id')
        user: User = await get_user_by_id(user_id, session)
        await session.delete(user)
        await session.commit()
        user_service_logger.info('User successfully deleted')
    except SQLAlchemyError as e:
        user_service_logger.exception('Exception with db:')
        raise e

async def get_all_users(session: AsyncSession) -> list[OutputUserSchema]:
    try:
        stmt = select(User)
        result: Result = await session.execute(stmt)
        users: list[User] = list(result.scalars().all())

        return [OutputUserSchema(**user.model_dump()) for user in users]

    except SQLAlchemyError as e:
        user_service_logger.exception('Exception with db:')
        raise e