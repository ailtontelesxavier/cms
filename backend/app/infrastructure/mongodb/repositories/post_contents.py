from datetime import datetime
from typing import Any

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase


class PostContentRepository:
    def __init__(self, db: AsyncIOMotorDatabase) -> None:
        self.collection = db.post_contents

    def _to_object_id(self, object_id: str | ObjectId) -> ObjectId:
        return object_id if isinstance(object_id, ObjectId) else ObjectId(object_id)

    async def create(self, post_ref_id: str, html: str, plain_text: str = "", summary: str = "", document_id: str | None = None) -> ObjectId | str:
        doc: dict[str, Any] = {
            "post_ref_id": post_ref_id,
            "html": html,
            "plain_text": plain_text,
            "summary": summary,
            "cover_image": None,
            "images": [],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }
        if document_id:
            doc["_id"] = document_id
        result = await self.collection.insert_one(doc)
        return result.inserted_id

    async def get(self, object_id: str | ObjectId) -> dict[str, Any] | None:
        return await self.collection.find_one({"_id": self._to_object_id(object_id)})

    async def get_by_post_ref(self, post_ref_id: str) -> dict[str, Any] | None:
        return await self.collection.find_one({"post_ref_id": post_ref_id})

    async def update(self, object_id: str | ObjectId, data: dict[str, Any]) -> bool:
        data["updated_at"] = datetime.utcnow()
        result = await self.collection.update_one(
            {"_id": self._to_object_id(object_id)}, {"$set": data}
        )
        return result.modified_count > 0

    async def delete(self, object_id: str | ObjectId) -> bool:
        result = await self.collection.delete_one({"_id": self._to_object_id(object_id)})
        return result.deleted_count > 0

    async def add_image(self, object_id: str | ObjectId, image: dict[str, Any]) -> bool:
        result = await self.collection.update_one(
            {"_id": self._to_object_id(object_id)},
            {
                "$push": {"images": image},
                "$set": {"updated_at": datetime.utcnow()},
            },
        )
        return result.modified_count > 0

    async def remove_image(self, object_id: str | ObjectId, object_key: str) -> bool:
        result = await self.collection.update_one(
            {"_id": self._to_object_id(object_id)},
            {
                "$pull": {"images": {"object_key": object_key}},
                "$set": {"updated_at": datetime.utcnow()},
            },
        )
        return result.modified_count > 0
