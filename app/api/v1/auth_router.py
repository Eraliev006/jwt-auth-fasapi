from typing import Annotated

from fastapi import APIRouter, Form
from fastapi.params import Depends
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.background import BackgroundTasks

from app.core import db_helper, security
from app.exceptions import UserNotVerifiedEmail, UserWithEmailNotFound
from app.schemas import CreateUserSchema, LoginUserSchema, OutputUserSchema, ErrorResponse, LoginOutputSchema
from app.services import register_user, verify_user, login_user, get_user_by_email, refresh_pair_of_tokens

router = APIRouter(
    tags=['JWT Auth'],
    prefix='/auth'
)

SESSION_DEP = Annotated[AsyncSession, Depends(db_helper.session_getter)]
async def check_is_user_verify_email(user_login: Annotated[LoginUserSchema, Form()], session: SESSION_DEP):
    user = await get_user_by_email(user_login.email, session)
    if not user:
        raise UserWithEmailNotFound
    if not user.is_verified:
        raise UserNotVerifiedEmail


@router.post(
    '/register',
    response_model=OutputUserSchema,
    status_code=status.HTTP_201_CREATED,
    responses={
      400: {
            "model": ErrorResponse,
            "description": "Email already registered"
      },
      500: {
          "model": ErrorResponse,
        "description": "Internal Server Error"
     }
    },
    summary='Register new user',
    description='Register new user. After you should verify your email than login'
)
async def register_user_route(user: CreateUserSchema, session: SESSION_DEP, background_tasks: BackgroundTasks):
    return await register_user(user, session, background_tasks)

@router.post(
    '/login',
    response_model=LoginOutputSchema,
    status_code=status.HTTP_200_OK,
    responses={
        403: {
            "model": ErrorResponse,
            "description": "User has not verified their email"
        },
        401: {
            "model": ErrorResponse,
            "description": "Invalid username or password"
        },
        500: {
            "model": ErrorResponse,
            "description": "Internal Server Error"
        }
    },
    dependencies=[Depends(check_is_user_verify_email)],
    summary='Login in app',
    description='Login in app. You should already verify your email. Than you`ll get a pairs of tokens'
)
async def login_user_route(user_login: Annotated[LoginUserSchema, Form()], session: SESSION_DEP):
    return await login_user(user_login, session)

@router.get('/verify-email')
async def verify_email(token: str, session: SESSION_DEP):
    return await verify_user(token, session)

@router.get(
    '/refresh',
    response_model=LoginOutputSchema,
    responses={
        401: {
            "model": ErrorResponse,
            "description": "Invalid or expired refresh token"
        },
        403: {
            "model": ErrorResponse,
            "description": "Refresh token is missing"
        },
        500: {
            "model": ErrorResponse,
            "description": "Internal Server Error"
        }
    },
    status_code=status.HTTP_200_OK,
    summary='Refresh your refresh_token',
    description='Refresh your refresh_token. You should send your refresh token,than you`ll get new pairs of tokens'
)
async def refresh_token(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]
):
    return await refresh_pair_of_tokens(credentials)

