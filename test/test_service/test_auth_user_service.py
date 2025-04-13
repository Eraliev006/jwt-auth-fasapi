from unittest.mock import patch

import pytest

from app.exceptions import UserWithEmailAlreadyExists, UserWithEmailNotFound, PasswordIsIncorrect
from app.schemas import CreateUserSchema, OutputUserSchema, LoginUserSchema
from app.services import register_user, login_user
from test.utils.utils import random_lower_string, random_email

async def __register_user(db_session, background_tasks):
    user_data = CreateUserSchema(
        name = random_lower_string(),
        email = random_email(),
        avatar_url = random_lower_string(),
        password = random_lower_string()
    )
    with patch("app.services.auth_service.send_email", return_value=None):
        registered_user: OutputUserSchema = await register_user(user_data, db_session,background_tasks)
        return {
            'registered_user': registered_user,
            'user_data': user_data
        }


@pytest.mark.asyncio
async def test_register_user_success(db_session, background_tasks):

    users = await __register_user(db_session, background_tasks)
    registered_user = users['registered_user']

    assert isinstance(registered_user, OutputUserSchema)
    assert not hasattr(registered_user, 'password_hash')
    assert registered_user.email
    assert registered_user.is_verified == False, 'after creating user by default user if not verified'

@pytest.mark.asyncio
async def test_register_user_failed_email_already_registered(db_session, background_tasks):
    users = await __register_user(db_session, background_tasks)
    user_data = users['user_data']

    with pytest.raises(UserWithEmailAlreadyExists):
        await register_user(user_data, db_session, background_tasks)

@pytest.mark.asyncio
async def test_login_user_failed_email_not_found(db_session):
    login_user_data = LoginUserSchema(
        email = random_email(),
        password = random_lower_string()
    )
    with pytest.raises(UserWithEmailNotFound):
        await login_user(login_user_data, db_session)

@pytest.mark.asyncio
async def test_login_user_failed_password_is_incorrect(db_session, background_tasks):
    users = await __register_user(db_session, background_tasks)
    user_data: CreateUserSchema = users['user_data']
    login_user_data = LoginUserSchema(
        email = user_data.email,
        password = 'incorrect password' + random_lower_string(),
    )
    with pytest.raises(PasswordIsIncorrect):
        await login_user(login_user_data, db_session)


