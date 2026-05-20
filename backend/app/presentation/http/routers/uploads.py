from uuid import UUID

import magic
from fastapi import APIRouter, Depends, File, UploadFile

from app.application.posts.ports import ObjectStorage, PostContentRepository, PostRepository
from app.core.exceptions import ValidationError
from app.core.security import generate_safe_filename
from app.domain.auth.entities import User
from app.infrastructure.minio.storage import MinioObjectStorage
from app.infrastructure.mongodb.client import get_mongo_db
from app.infrastructure.mongodb.repositories.post_contents import (
    PostContentRepository as MongoPostContentRepo,
)
from app.infrastructure.postgres.database import get_session
from app.infrastructure.postgres.repositories.posts import PostRepository as PGPostRepository
from app.infrastructure.redis.rate_limit import limiter
from app.presentation.http.dependencies import get_current_user, require_permission

router = APIRouter(prefix="/posts/{post_id}/images", tags=["uploads"])

ALLOWED_MIMES = {"image/jpeg", "image/png", "image/webp"}


async def get_post_repo(session=Depends(get_session)) -> PostRepository:
    return PGPostRepository(session)


async def get_content_repo() -> PostContentRepository:
    db = await get_mongo_db()
    return MongoPostContentRepo(db)


def get_storage() -> ObjectStorage:
    return MinioObjectStorage()


@router.post("")
@limiter.limit("30/minute")
async def upload_image(
    post_id: UUID,
    file: UploadFile = File(...),
    _=Depends(require_permission("posts", "atualizar")),
    current_user: User = Depends(get_current_user),
    post_repo: PostRepository = Depends(get_post_repo),
    content_repo: PostContentRepository = Depends(get_content_repo),
    storage: ObjectStorage = Depends(get_storage),
    request=None,
):
    content = await file.read()
    detected_mime = magic.from_buffer(content, mime=True)
    if detected_mime not in ALLOWED_MIMES:
        raise ValidationError(f"Invalid MIME type: {detected_mime}. Allowed: {ALLOWED_MIMES}")

    post = await post_repo.get_by_id(post_id)
    if not post:
        from app.domain.posts.exceptions import PostNotFoundError
        raise PostNotFoundError(str(post_id))

    safe_name = generate_safe_filename()
    ext = file.filename.rsplit(".", 1)[-1] if "." in file.filename else "bin"
    object_key = f"upload/post/{post.mongo_object_id}/{safe_name}.{ext}"
    url = await storage.put_object(object_key, content, detected_mime)

    image_data = {
        "object_key": object_key,
        "content_type": detected_mime,
        "size": len(content),
        "alt": file.filename or "",
    }
    await content_repo.add_image(post.mongo_object_id, image_data)

    return {"image_id": safe_name, "object_key": object_key, "url": url}


@router.get("/{img_id}/download")
async def download_image(
    post_id: UUID,
    img_id: str,
    storage: ObjectStorage = Depends(get_storage),
    post_repo: PostRepository = Depends(get_post_repo),
):
    post = await post_repo.get_by_id(post_id)
    if not post:
        from app.domain.posts.exceptions import PostNotFoundError
        raise PostNotFoundError(str(post_id))
    url = await storage.get_presigned_url(f"upload/post/{post.mongo_object_id}/{img_id}")
    return {"url": url}


@router.delete("/{img_id}")
async def delete_image(
    post_id: UUID,
    img_id: str,
    _=Depends(require_permission("posts", "atualizar")),
    post_repo: PostRepository = Depends(get_post_repo),
    content_repo: PostContentRepository = Depends(get_content_repo),
    storage: ObjectStorage = Depends(get_storage),
):
    post = await post_repo.get_by_id(post_id)
    if not post:
        from app.domain.posts.exceptions import PostNotFoundError
        raise PostNotFoundError(str(post_id))

    object_key = f"upload/post/{post.mongo_object_id}/{img_id}"
    await storage.delete_object(object_key)
    await content_repo.remove_image(post.mongo_object_id, object_key)
    return {"deleted": True}
