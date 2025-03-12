from logging import getLogger

import uvicorn
from fastapi import FastAPI

from core import settings
import logger

app = FastAPI()

main_logger = getLogger('project.main')


if __name__ == "__main__":
    main_logger.info('Server start')
    uvicorn.run('main:app', host=settings.HOST, port=settings.PORT, reload=False)
    main_logger.info('Server stopped')