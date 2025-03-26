from urllib.parse import urlencode

from app.core import settings


def generate_verify_link(token: str) -> str:
    params = urlencode({'token': token})
    return f"{settings.BASE_URL}/auth/verify-email/?{params}"
