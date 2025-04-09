from typing import Annotated

from fastapi import APIRouter, Form
from fastapi.params import Depends
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import db_helper, security
from app.exceptions import UserNotVerifiedEmail
from app.schemas import CreateUserSchema, LoginUserSchema
from app.services import register_user, verify_user, login_user, get_user_by_email, refresh_pair_of_tokens

router = APIRouter(
    tags=['JWT Auth'],
    prefix='/auth'
)

SESSION_DEP = Annotated[AsyncSession, Depends(db_helper.session_getter)]
async def check_is_user_verify_email(user_login: LoginUserSchema, session: SESSION_DEP):
    user = await get_user_by_email(user_login.email, session)
    if not user.is_verified:
        raise UserNotVerifiedEmail


@router.post('/register')
async def register_user_route(user: CreateUserSchema, session: SESSION_DEP):
    return await register_user(user, session)

@router.post('/login', dependencies=[Depends(check_is_user_verify_email)])
async def login_user_route(user_login: Annotated[LoginUserSchema, Form()], session: SESSION_DEP):
    return await login_user(user_login, session)

@router.get('/verify-email')
async def verify_email(token: str, session: SESSION_DEP):
    return await verify_user(token, session)

@router.get('/refresh')
async def refresh_token(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]
):
    return await refresh_pair_of_tokens(credentials)

