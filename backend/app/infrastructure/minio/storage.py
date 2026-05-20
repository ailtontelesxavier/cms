from app.core.config import settings
from app.infrastructure.minio import S3Error
from app.infrastructure.minio.client import get_minio_client


class MinioObjectStorage:
    def __init__(self) -> None:
        self.client = get_minio_client()
        self.bucket = settings.minio_bucket

    async def put_object(self, key: str, data: bytes, content_type: str) -> str:
        self.client.put_object(
            bucket_name=self.bucket,
            object_name=key,
            data=__import__("io").BytesIO(data),
            length=len(data),
            content_type=content_type,
        )
        return f"{settings.minio_public_url}/{key}"

    async def get_presigned_url(self, key: str) -> str:
        return self.client.presigned_get_object(self.bucket, key)

    async def delete_object(self, key: str) -> None:
        from contextlib import suppress
        with suppress(S3Error):
            self.client.remove_object(self.bucket, key)
