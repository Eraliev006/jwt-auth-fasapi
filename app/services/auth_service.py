from logging import getLogger
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import UserWithEmailAlreadyExists
from app.models import User
from app.schemas import CreateUserSchema, OutputUserSchema
from app.services import send_email, create_user
from app.services import get_user_by_email
from app.utils import generate_email_verify_token, generate_verify_link
from app.utils import hash_password

from logging_config import setup_logging

setup_logging()
auth_service_logger = getLogger('project.auth_service')

async def register_user(user: CreateUserSchema, session: AsyncSession) -> OutputUserSchema:
    auth_service_logger.info('Checking is user with email already exists')
    exists_user: Optional[User] = await get_user_by_email(user.email, session)

    if exists_user is not None:
        auth_service_logger.error('User with same email already exists')
        raise UserWithEmailAlreadyExists(f'User with email {user.email} already exists')

    hashed_password: str = hash_password(user.password)

    auth_service_logger.info('Call create user method')

    created_user: Optional[OutputUserSchema] = await create_user(
        session,
        User(
            **user.model_dump(exclude={'password'}),
            password_hash=hashed_password
        )
    )

    auth_service_logger.info('Create user method finished')

    email = created_user.email

    auth_service_logger.info('Call send email function')

    token = generate_email_verify_token({'sub': email,'user_id': created_user.id})
    link = generate_verify_link(token)
    send_email(email, 'Confirm email',
               body=f"Hello press the link to confirm your gmail: {link}")

    auth_service_logger.info('email function ended')

    return created_user

