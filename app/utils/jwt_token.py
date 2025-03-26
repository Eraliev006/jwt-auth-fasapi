from datetime import datetime, timezone
from logging import getLogger
from typing import Any

import jwt
from datetime import timedelta

from app.core import settings
from app.exceptions import ExpireSignatureError, InvalidTokenError
from logging_config import setup_logging

setup_logging()
jwt_token_utils_logger = getLogger('project.jwt_token_utils')

def generate_email_verify_token(
        payload: dict[str, Any],
        secret_key: str = settings.jwt.secret_key,
        algorithm: str = settings.jwt.algorithm,
) -> str:
    jwt_token_utils_logger.info('Generate email verify token')
    payload = {
        **payload,
        'exp': datetime.now(timezone.utc) + timedelta(minutes=settings.jwt.email_token_expire_minutes)
    }
    token = jwt.encode(
        payload = payload,
        key = secret_key,
        algorithm = algorithm
    )
    jwt_token_utils_logger.info('Return email verify token')

    return token

def decode_jwt_token(
        token: str,
        secret_key: str = settings.jwt.secret_key,
        algorithm: str = settings.jwt.algorithm,
) -> dict[str, Any]:
    try:
        decoded = jwt.decode(
            token,
            key=secret_key,
            algorithms=algorithm
        )
        return decoded
    except jwt.ExpiredSignatureError:
        jwt_token_utils_logger.exception('Token has expired.')
        raise ExpireSignatureError('Token has expired.')
    except jwt.InvalidTokenError:
        jwt_token_utils_logger.exception('Token is invalid.')
        raise InvalidTokenError('Token is invalid.')
