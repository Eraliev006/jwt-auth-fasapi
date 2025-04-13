from datetime import timedelta
from logging import getLogger

import redis.asyncio as redis

from app.core import settings

redis_logger = getLogger('project.redis_client')

class RedisClient:
    def __init__(self, host:str, port: int, decode_response: bool = True):
        redis_logger.info('Initialize a redis connect')
        self.redis_client = redis.Redis(
            host=host,
            port=port,
            decode_responses=decode_response
        )

    async def set_data(self, key: str, value:str, expire: int | timedelta):
        redis_logger.info('Create new data in redis')
        return await self.redis_client.set(
            name=key,
            value=value,
            ex=expire
        )

    async def get_data(self, key: str) -> str | None:
        redis_logger.info('Get data from redis')
        return await self.redis_client.get(name=key)

    async def delete_data(self, key: str | list[str]) -> None:
        if isinstance(key, list):
            return await self.redis_client.delete(*key)
        return await self.redis_client.delete(key)

    async def dispose(self):
        redis_logger.info('Dispose connection with redis')
        return await self.redis_client.aclose()


redis_client = RedisClient(settings.redis.redis_host, settings.redis.redis_port)
