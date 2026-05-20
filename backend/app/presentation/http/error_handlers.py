from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exceptions import (
    DomainError,
    DuplicateError,
    ForbiddenError,
    NotFoundError,
    UnauthorizedError,
    ValidationError,
)


async def domain_error_handler(request: Request, exc: DomainError) -> JSONResponse:
    if isinstance(exc, NotFoundError):
        return JSONResponse(status_code=404, content={"detail": str(exc)})
    if isinstance(exc, DuplicateError):
        return JSONResponse(status_code=409, content={"detail": str(exc)})
    if isinstance(exc, UnauthorizedError):
        return JSONResponse(status_code=401, content={"detail": str(exc)})
    if isinstance(exc, ForbiddenError):
        return JSONResponse(status_code=403, content={"detail": str(exc)})
    if isinstance(exc, ValidationError):
        return JSONResponse(status_code=422, content={"detail": str(exc)})
    return JSONResponse(status_code=400, content={"detail": str(exc)})
