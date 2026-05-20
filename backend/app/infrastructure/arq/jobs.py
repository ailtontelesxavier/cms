from datetime import datetime, timedelta


async def cleanup_orphan_contents(ctx: dict) -> None:
    db = ctx["mongo_db"]
    cutoff = datetime.utcnow() - timedelta(hours=24)
    result = await db.post_contents.delete_many({
        "post_ref_id": "",
        "created_at": {"$lt": cutoff},
    })
    if result.deleted_count:
        print(f"Cleaned up {result.deleted_count} orphan post contents")


async def cleanup_orphan_images(ctx: dict) -> None:
    db = ctx["mongo_db"]
    minio = ctx["minio"]
    bucket = ctx.get("bucket", "cms-images")

    cursor = db.post_contents.find({"images": {"$exists": True, "$ne": []}})
    async for doc in cursor:
        for img in doc.get("images", []):
            key = img.get("object_key", "")
            if key:
                try:
                    minio.stat_object(bucket, key)
                except Exception:
                    await db.post_contents.update_one(
                        {"_id": doc["_id"]},
                        {"$pull": {"images": {"object_key": key}}},
                    )
