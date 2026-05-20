from app.core.config import settings
from app.infrastructure.minio import Minio

_minio_client: Minio | None = None


def get_minio_client() -> Minio:
    global _minio_client
    if _minio_client is None:
        _minio_client = Minio(
            endpoint=settings.minio_endpoint,
            access_key=settings.minio_access_key,
            secret_key=settings.minio_secret_key,
            secure=settings.minio_use_ssl,
        )
        bucket = settings.minio_bucket
        if not _minio_client.bucket_exists(bucket):
            _minio_client.make_bucket(bucket)
    return _minio_client
