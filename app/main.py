from contextlib import asynccontextmanager
from logging import getLogger

import uvicorn
from fastapi import FastAPI

from app.core import db_helper
from core import settings
from api import router
import logger

main_logger = getLogger('project.main')

@asynccontextmanager
async def lifespan(app:FastAPI):
    yield

    # dispose connection with db
    main_logger.info('dispose connection with db')
    db_helper.dispose()

app = FastAPI(lifespan=lifespan)
app.include_router(router)

if __name__ == "__main__":
    main_logger.info('Server start')
    uvicorn.run('main:app', host=settings.HOST, port=settings.PORT, reload=False)
    main_logger.info('Server stopped')