from uuid import uuid4

from loguru import logger as loguru_logger
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid4())
        request.state.request_id = request_id
        with loguru_logger.contextualize(request_id=request_id):
            response = await call_next(request)
        return response
