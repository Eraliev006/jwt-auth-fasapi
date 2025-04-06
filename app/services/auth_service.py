import datetime
import enum
from datetime import timedelta
from logging import getLogger
from typing import Optional, Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import UserWithEmailAlreadyExists, UserWithEmailNotFound, PasswordIsIncorrect
from app.models import User
from app.schemas import CreateUserSchema, OutputUserSchema, LoginUserSchema, LoginOutputSchema
from app.services import send_email, create_user, get_user_by_id
from app.services import get_user_by_email
from app.services.user_service import change_user_verify_status
from app.utils import generate_email_verify_token, generate_verify_link, decode_jwt_token, password_is_correct, \
    create_token
from app.utils import hash_password

from logging_config import setup_logging

setup_logging()
auth_service_logger = getLogger('project.auth_service')

class TokenType(enum.Enum):
    ACCESS = 'access'
    REFRESH = 'refresh'

async def register_user(user: CreateUserSchema, session: AsyncSession) -> OutputUserSchema:
    auth_service_logger.info('Register user')

    auth_service_logger.info('Checking is user with email already exists')
    exists_user: Optional[User] = await get_user_by_email(user.email, session)

    if exists_user is not None:
        auth_service_logger.error('User with same email already exists')
        raise UserWithEmailAlreadyExists(f'User with email {user.email} already exists')

    hashed_password: bytes = hash_password(user.password)
    hashed_password: str = hashed_password.decode()

    auth_service_logger.info('Call create user method')

    created_user: Optional[User] = await create_user(
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

    auth_service_logger.info('Register function is end')
    return OutputUserSchema(**created_user.model_dump())

async def verify_user(token: str, session: AsyncSession) -> OutputUserSchema:
    auth_service_logger.info('Verifying user')
    payload: dict[str, Any] = decode_jwt_token(
        token,
    )
    user_id: int = payload['user_id']
    user: User = await get_user_by_id(user_id, session)
    await change_user_verify_status(user, session)
    auth_service_logger.info('User verifying status changed to True')
    return OutputUserSchema(**user.model_dump())

async def login_user(user_login: LoginUserSchema, session: AsyncSession) -> LoginOutputSchema:
    auth_service_logger.info('Login user')
    email, password = user_login.email, user_login.password

    user = await get_user_by_email(email, session)
    if user is None:
        auth_service_logger.error('User with this email is not exists')
        raise UserWithEmailNotFound(f'User with email-{email} not found')

    user_password = user.password_hash

    is_password_correct:bool = password_is_correct(password.encode(), user_password.encode())
    auth_service_logger.debug(f'{is_password_correct=}')

    if not is_password_correct:
        auth_service_logger.error('Password is incorrect')
        raise PasswordIsIncorrect('Password is incorrect')

    payload = {
        'sub': user,
    }

    access_token = create_token(
        payload={
            **payload,
            'exp': datetime.datetime.now(datetime.UTC) + timedelta(minutes=1),
            'type': TokenType.ACCESS,
        }
    )
    refresh_token = create_token(
        payload={
            **payload,
            'exp': datetime.datetime.now(datetime.UTC) + timedelta(minutes=3),
            'type': TokenType.ACCESS,
        }
    )

    return LoginOutputSchema(
        refresh_token = refresh_token,
        access_token = access_token
    )