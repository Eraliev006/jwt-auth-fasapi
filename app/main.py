from contextlib import asynccontextmanager
from logging import getLogger

import uvicorn
from fastapi import FastAPI

from app.core import db_helper
from app.utils import redis_client
from core import settings
from api import router

from logging_config import setup_logging

setup_logging()

main_logger = getLogger('project.main')

@asynccontextmanager
async def lifespan(app:FastAPI):
    try:
        pong = await redis_client.redis_client.ping()
        if pong:
            main_logger.info("Redis is alive ✅")
    except Exception as e:
        main_logger.warning(f"Redis connection failed: {e}")

    yield

    # dispose connection with db
    main_logger.info('dispose connection with db')
    await db_helper.dispose()

    # dispose connection with redis
    main_logger.info('dispose connection with redis')
    await redis_client.dispose()

app = FastAPI(lifespan=lifespan)
app.include_router(router)

if __name__ == "__main__":
    main_logger.info('Server start')
    uvicorn.run('main:app', host=settings.HOST, port=settings.PORT, reload=False)
    main_logger.info('Server stopped')