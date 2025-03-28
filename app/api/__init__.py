from fastapi import APIRouter

from app.core import settings
from .v1.auth_router import router as auth_router
from .v1.user_router import router as user_router

router = APIRouter(
    prefix=settings.api_prefix
)

router.include_router(auth_router)
router.include_router(user_router)