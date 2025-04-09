from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import db_helper
from app.core.security import get_current_user
from app.schemas import OutputUserSchema

router = APIRouter(
    tags=['USER'],
    prefix = '/users'
)

SESSION_DEP = Annotated[AsyncSession, Depends(db_helper.session_getter)]
CURRENT_USER_DEP = Annotated[OutputUserSchema, Depends(get_current_user)]
@router.get("/me")
def read_current_user(
        current_user: CURRENT_USER_DEP
):
    return current_user