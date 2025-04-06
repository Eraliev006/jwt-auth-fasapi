from typing import Annotated

from fastapi import APIRouter, Form
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import db_helper
from app.exceptions import UserWithIdNotFound, UserNotVerifyEmail
from app.schemas import CreateUserSchema, LoginUserSchema
from app.services import register_user, verify_user, login_user, get_user_by_email

router = APIRouter(
    tags=['JWT Auth'],
    prefix='/auth'
)

SESSION_DEP = Annotated[AsyncSession, Depends(db_helper.session_getter)]
async def check_is_user_verify_email(user_login: LoginUserSchema, session: SESSION_DEP):
    user = await get_user_by_email(user_login.email, session)
    if not user:
        raise UserWithIdNotFound('User with email not found')

    if not user.is_verified:
        raise UserNotVerifyEmail('Please first verify your email')


@router.post('/register')
async def register_user_route(user: CreateUserSchema, session: SESSION_DEP):
    return await register_user(user, session)

@router.post('/login', dependencies=[Depends(check_is_user_verify_email)])
async def login_user_route(user_login: Annotated[LoginUserSchema, Form()], session: SESSION_DEP):
    return await login_user(user_login, session)

@router.get('/verify-email')
async def verify_email(token: str, session: SESSION_DEP):
    return await verify_user(token, session)

