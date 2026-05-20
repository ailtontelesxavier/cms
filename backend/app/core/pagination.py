from collections.abc import Sequence
from math import ceil
from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class PaginatedParams:
    def __init__(self, page: int = 1, page_size: int = 20) -> None:
        self.page = max(1, page)
        self.page_size = min(100, max(1, page_size))

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size

    @property
    def limit(self) -> int:
        return self.page_size


class PaginatedResult(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    page_size: int
    pages: int

    @classmethod
    def create(cls, items: Sequence[T], total: int, params: PaginatedParams) -> "PaginatedResult[T]":
        return cls(
            items=list(items),
            total=total,
            page=params.page,
            page_size=params.page_size,
            pages=max(1, ceil(total / params.page_size)),
        )
