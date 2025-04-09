from fastapi import HTTPException
from starlette.status import HTTP_403_FORBIDDEN


class AuthException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=HTTP_403_FORBIDDEN,
            detail=detail
        )


class ExpiredSignatureError(AuthException):
    def __init__(self):
        super().__init__("Token has expired")


class InvalidTokenError(AuthException):
    def __init__(self):
        super().__init__("Invalid token")


class InvalidSignatureError(AuthException):
    def __init__(self):
        super().__init__("Invalid signature")


class PasswordIsIncorrect(AuthException):
    def __init__(self):
        super().__init__("Password is incorrect")


class UserNotVerifiedEmail(AuthException):
    def __init__(self):
        super().__init__("User has not verified their email")


class InvalidTokenType(AuthException):
    def __init__(self):
        super().__init__("Invalid token type")


class RefreshTokenDoesNotExist(AuthException):
    def __init__(self):
        super().__init__("Refresh token does not exist")
