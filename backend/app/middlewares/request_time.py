import time

from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


class RequestTimeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        duration_ms = (time.perf_counter() - start) * 1000
        logger.info(
            "{method} {path} {status} {duration:.0f}ms",
            method=request.method,
            path=request.url.path,
            status=response.status_code,
            duration=duration_ms,
        )
        if duration_ms > 1000:
            logger.warning("Slow request ({duration:.0f}ms): {method} {path}",
                           duration=duration_ms, method=request.method, path=request.url.path)
        return response
