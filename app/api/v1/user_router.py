from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import db_helper
from app.services import delete_user, get_all_users

router = APIRouter(
    tags=['USER'],
    prefix = '/users'
)

SESSION_DEP = Annotated[AsyncSession, Depends(db_helper.session_getter)]

@router.delete('/{user_id}')
async def delete(user_id: int, session: SESSION_DEP) -> None:
    return await delete_user(user_id, session)

@router.get('/')
async def get_all(session: SESSION_DEP):
    return await get_all_users(session)