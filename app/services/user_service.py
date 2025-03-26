from logging import getLogger
from typing import Optional
from urllib.parse import urlencode

import bcrypt
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.core import settings
from app.exceptions import UserWithEmailAlreadyExists
from app.models import User
from app.services import send_email
from app.utils import generate_verify_link, generate_email_verify_token
from logging_config import setup_logging
from app.schemas import CreateUserSchema, OutputUserSchema

setup_logging()
user_service_logger = getLogger('project.user_service')

def _hash_password(password: str) -> str:
    user_service_logger.info('Hashing password')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()

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

def _send_email(email: str, user_id: int):
    token = generate_email_verify_token({'sub': email,'user_id': int})
    link = generate_verify_link(token)
    send_email(email, 'Confirm email',
               body=f"Hello press the link to confirm your gmail: {link}")


async def create_user(session: AsyncSession, user: CreateUserSchema) -> OutputUserSchema:
    user_service_logger.info('creating user, and save to db')

    try:
        exists_user = await get_user_by_email(user.email, session)
        if exists_user is not None:
            user_service_logger.error('User with same email already exists')
            raise UserWithEmailAlreadyExists(f'User with email {user.email} already exists')

        hashed_password: str = _hash_password(password=user.password)

        user = User(
            **user.model_dump(exclude={'password'}),
            password_hash = hashed_password
        )

        user_service_logger.info('Call send email function')

        _send_email(user.email, user.id)

        user_service_logger.info('email function ended')

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