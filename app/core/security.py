from typing import Annotated

from fastapi.params import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core import db_helper
from app.exceptions import InvalidTokenType
from app.schemas import OutputUserSchema
from app.services import get_user_by_id
from app.utils import decode_jwt_token

security = HTTPBearer()

async def get_current_user(
        credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
) -> OutputUserSchema:
    token = credentials.credentials
    print(f'{token=}')
    payload = decode_jwt_token(token)

    if payload.get("type") != "access":
        raise InvalidTokenType()

    user_id:int = int(payload.get("sub"))
    user = await get_user_by_id(user_id, session)


    return OutputUserSchema(**user.model_dump())


