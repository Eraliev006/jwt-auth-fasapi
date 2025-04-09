from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.core import db_helper
from app.core.security import get_current_user
from app.schemas import OutputUserSchema, ErrorResponse

router = APIRouter(
    tags=['USER'],
    prefix = '/users'
)

SESSION_DEP = Annotated[AsyncSession, Depends(db_helper.session_getter)]
CURRENT_USER_DEP = Annotated[OutputUserSchema, Depends(get_current_user)]
@router.get(
    "/me",
    response_model=OutputUserSchema,
    status_code=status.HTTP_200_OK,
    responses={
        403: {
            "model": ErrorResponse,
            "description": 'Not authorized'
        }
    },
    summary='Get current user',
    description='To get current user, you should login and send your access_token in headers Bearer<access_token>'
)
def read_current_user(
        current_user: CURRENT_USER_DEP
):
    return current_user