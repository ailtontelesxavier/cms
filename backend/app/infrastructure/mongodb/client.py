from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.core.config import settings

_mongo_client: AsyncIOMotorClient | None = None


async def get_mongo_client() -> AsyncIOMotorClient:
    global _mongo_client
    if _mongo_client is None:
        _mongo_client = AsyncIOMotorClient(settings.mongodb_url)
    return _mongo_client


async def get_mongo_db() -> AsyncIOMotorDatabase:
    client = await get_mongo_client()
    return client[settings.mongodb_db_name]


async def close_mongo_client() -> None:
    global _mongo_client
    if _mongo_client:
        _mongo_client.close()
        _mongo_client = None


async def ensure_mongo_indexes() -> None:
    db = await get_mongo_db()
    await db.post_contents.create_index("post_ref_id", unique=True)
    await db.post_contents.create_index("updated_at")
