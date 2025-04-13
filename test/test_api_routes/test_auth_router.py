from unittest.mock import patch, AsyncMock

from app.api.v1.auth_router import check_is_user_verify_email, refresh_token
from app.core import settings
from app.main import app
from app.models import User
from app.schemas import CreateUserSchema, LoginUserSchema, LoginOutputSchema
from app.services import get_user_by_email
from test.utils.utils import random_lower_string, random_email

async def test_register_user(client, db_session):
    body_data = CreateUserSchema(
        name = random_lower_string(),
        email = random_email(),
        avatar_url = random_lower_string(),
        password = random_lower_string()
    )
    with patch('app.services.auth_service.send_email'):
        response = client.post(
            f'{settings.api_prefix}/auth/register',
            json=body_data.model_dump()
        )
        assert 200 <= response.status_code < 300, 'response_status code should be 2xx'
        created_user = response.json()
        user = await get_user_by_email(body_data.email, db_session)
        assert user, 'have not be None'
        assert created_user['email'] == user.email

def test_register_user_email_already_exists(client, db_session):
    body_data = CreateUserSchema(
        name = random_lower_string(),
        email = random_email(),
        avatar_url = random_lower_string(),
        password = random_lower_string()
    )
    with patch('app.services.auth_service.send_email'):
        client.post(
            f'{settings.api_prefix}/auth/register',
            json=body_data.model_dump()
        )
        response_2 = client.post(
            f'{settings.api_prefix}/auth/register',
            json=body_data.model_dump()
        )
        error_msg: dict = response_2.json()
        assert error_msg['detail'] == "User with this email already exists"
        assert 400 <= response_2.status_code < 500


def test_verify_email(client):
    fake_user_data = User(
        id = 1,
        name = random_lower_string(),
        email = random_email(),
        avatar_url = random_lower_string(),
        password = random_lower_string()
    )

    with (
            patch('app.services.auth_service.decode_jwt_token', return_value={'user_id': 1}),
            patch('app.services.auth_service.get_user_by_id', new_callable=AsyncMock, return_value=fake_user_data),
    ):
        response = client.get(
            f"{settings.api_prefix}/auth/verify-email?token=mocked_token"
        )
        assert 200 <= response.status_code < 300
        assert fake_user_data.is_verified is True, 'User should be marked as verified'

def test_login_user_success(client, fake_login_user_data):

    async def mock_check_is_user_verify_email():
        pass

    app.dependency_overrides[check_is_user_verify_email] = mock_check_is_user_verify_email

    mock_response_json = LoginOutputSchema(
        access_token = 'access_token',
        refresh_token = 'refresh_token',
        token_type = 'Bearer'
    )

    with patch('app.api.v1.auth_router.login_user', return_value = mock_response_json):

        response = client.post(
            f"{settings.api_prefix}/auth/login",
            data=fake_login_user_data
        )

        assert 200 <= response.status_code < 300
        assert 'access_token' in response.json()
        assert response.json() == mock_response_json.model_dump()

def test_login_user_failed_user_with_email_not_found(client, fake_login_user_data):
    response = client.post(
        f"{settings.api_prefix}/auth/login",
        data=fake_login_user_data
    )

    assert response.json() == {'detail': 'User with this email not found'}
    assert response.status_code == 404
