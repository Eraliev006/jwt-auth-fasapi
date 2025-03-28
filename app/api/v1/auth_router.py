from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import db_helper
from app.schemas import CreateUserSchema, LoginUserSchema
from app.services import register_user, verify_user

router = APIRouter(
    tags=['JWT Auth'],
    prefix='/auth'
)

SESSION_DEP = Annotated[AsyncSession, Depends(db_helper.session_getter)]

@router.post('/register')
async def register_user_route(user: CreateUserSchema, session: SESSION_DEP):
    return await register_user(user, session)

@router.post('/login')
async def login_user(user_login: LoginUserSchema, session: SESSION_DEP):
    pass

@router.get('/verify-email')
async def verify_email(token: str, session: SESSION_DEP):
    return await verify_user(token, session)

