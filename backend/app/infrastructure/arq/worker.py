from app.core.config import settings
from app.infrastructure.arq.jobs import cleanup_orphan_contents, cleanup_orphan_images


async def startup(ctx: dict) -> None:
    from app.infrastructure.minio import Minio
    from motor.motor_asyncio import AsyncIOMotorClient
    from redis.asyncio import Redis

    ctx["mongo"] = AsyncIOMotorClient(settings.mongodb_url)
    ctx["mongo_db"] = ctx["mongo"][settings.mongodb_db_name]
    ctx["redis"] = Redis.from_url(settings.redis_url)
    ctx["minio"] = Minio(
        settings.minio_endpoint,
        access_key=settings.minio_access_key,
        secret_key=settings.minio_secret_key,
        secure=settings.minio_use_ssl,
    )


async def shutdown(ctx: dict) -> None:
    if "mongo" in ctx:
        ctx["mongo"].close()
    if "redis" in ctx:
        await ctx["redis"].close()


class WorkerSettings:
    functions = [cleanup_orphan_contents, cleanup_orphan_images]
    redis_settings = {"redis_url": settings.redis_url}
    on_startup = startup
    on_shutdown = shutdown
    poll_delay = 10
