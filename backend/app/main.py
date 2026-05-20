from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.core.config import settings
from app.core.exceptions import DomainError
from app.core.logging import setup_logging
from app.infrastructure.mongodb.client import close_mongo_client, ensure_mongo_indexes
from app.infrastructure.redis.client import close_redis
from app.infrastructure.redis.rate_limit import limiter
from app.middlewares.request_context import RequestContextMiddleware
from app.middlewares.request_time import RequestTimeMiddleware
from app.presentation.http.error_handlers import domain_error_handler
from app.presentation.http.routers.auth import router as auth_router
from app.presentation.http.routers.health import router as health_router
from app.presentation.http.routers.posts import router as posts_router
from app.presentation.http.routers.tags import router as tags_router
from app.presentation.http.routers.uploads import router as uploads_router
from app.presentation.http.routers.users import router as users_router


@asynccontextmanager
async def lifespan(_app: FastAPI):
    setup_logging()
    await ensure_mongo_indexes()
    yield
    await close_mongo_client()
    await close_redis()


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RequestContextMiddleware)
app.add_middleware(RequestTimeMiddleware)

app.add_exception_handler(DomainError, domain_error_handler)

app.include_router(health_router, prefix="/api/v1")
app.include_router(auth_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")
app.include_router(tags_router, prefix="/api/v1")
app.include_router(posts_router, prefix="/api/v1")
app.include_router(uploads_router, prefix="/api/v1")
