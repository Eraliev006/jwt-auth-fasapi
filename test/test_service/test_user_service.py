import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import UserWithEmailNotFound, UserWithIdNotFound
from app.models import User
from app.services import create_user, get_user_by_email, get_user_by_id
from app.services.user_service import change_user_verify_status
from app.utils import hash_password
from test.utils.utils import random_lower_string, random_email

async def __create_user(db_session: AsyncSession) -> dict:
    user_data = {
        'name': random_lower_string(),
        'email': random_email(),
        'password_hash': hash_password(random_lower_string()).decode(),
        'avatar_url': random_lower_string(),
    }
    user = User(**user_data)
    created_user = await create_user(db_session, user)
    return {'created_user': created_user, 'user': user}

@pytest.mark.asyncio
async def test_create_user_success(db_session):
    users = await __create_user(db_session)
    user, created_user = users['user'], users['created_user']

    assert created_user.id is not None
    assert created_user.email == user.email
    assert created_user.is_verified == False


@pytest.mark.asyncio
async def test_create_user_failed_email_already_exists(db_session):
    users = await __create_user(db_session)
    user, created_user = users['user'], users['created_user']
    with pytest.raises(IntegrityError):
        await create_user(db_session, user)

@pytest.mark.asyncio
async def test_get_user_by_email_success(db_session):
    users = await __create_user(db_session)
    user, created_user = users['user'], users['created_user']

    user_by_email = await get_user_by_email(user.email, db_session)

    assert isinstance(user_by_email, User), 'result should be instance of User model'
    assert hasattr(user_by_email, 'id'), 'User has to have id field'
    assert user.email == created_user.email

@pytest.mark.asyncio
async def test_get_user_by_email_failed(db_session):
    await __create_user(db_session)

    with pytest.raises(UserWithEmailNotFound) as user_error:
        await get_user_by_email('Some another email', db_session)

@pytest.mark.asyncio
async def test_get_user_by_id_success(db_session):
    users = await __create_user(db_session)
    created_user = users['created_user']

    user_by_id = await get_user_by_id(created_user.id, session=db_session)

    assert user_by_id.id == created_user.id, 'after creating user_id should be'
    assert created_user.email == user_by_id.email
    assert isinstance(user_by_id, User)

@pytest.mark.asyncio
async def test_get_user_by_id_failed(db_session):
    non_exists_id = 999999

    with pytest.raises(UserWithIdNotFound):
        await get_user_by_id(non_exists_id, session=db_session)

@pytest.mark.asyncio
async def test_change_user_verify_status(db_session):
    users = await __create_user(db_session)
    created_user = users['created_user']

    await change_user_verify_status(created_user, db_session)

    assert created_user.is_verified == True

