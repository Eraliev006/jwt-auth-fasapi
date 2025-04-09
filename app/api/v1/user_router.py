from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import db_helper
from app.core.security import get_current_user
from app.schemas import OutputUserSchema
from app.services import delete_user, get_all_users

router = APIRouter(
    tags=['USER'],
    prefix = '/users'
)

SESSION_DEP = Annotated[AsyncSession, Depends(db_helper.session_getter)]
CURRENT_USER_DEP = Annotated[OutputUserSchema, Depends(get_current_user)]
@router.delete('/{user_id}')
async def delete(user_id: int, session: SESSION_DEP, current_user: CURRENT_USER_DEP) -> None:
    return await delete_user(user_id, session)

@router.get('/')
async def get_all(session: SESSION_DEP, current_user: CURRENT_USER_DEP):
    return await get_all_users(session)

@router.get("/me")
def read_current_user(
        current_user: CURRENT_USER_DEP
):
    return current_user