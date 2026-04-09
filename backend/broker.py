from taskiq_redis import ListQueueBroker, RedisAsyncResultBackend
from tortoise import Tortoise

from backend.config import TORTOISE_ORM, settings

result_backend = RedisAsyncResultBackend(redis_url=settings.REDIS_URL)

broker = ListQueueBroker(url=settings.REDIS_URL).with_result_backend(result_backend)


@broker.on_event("worker_startup")
async def _init_orm(state) -> None:  # noqa: ANN001
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()


@broker.on_event("worker_shutdown")
async def _close_orm(state) -> None:  # noqa: ANN001
    await Tortoise.close_connections()
