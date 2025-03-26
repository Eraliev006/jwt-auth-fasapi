from fastapi import APIRouter

from app.core import settings
from .v1.auth_router import router as auth_router

router = APIRouter(
    prefix=settings.api_prefix
)

router.include_router(auth_router)