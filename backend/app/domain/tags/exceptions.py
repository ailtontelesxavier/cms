from app.core.exceptions import DomainError


class TagNotFoundError(DomainError):
    def __init__(self, tag_id: int) -> None:
        super().__init__(f"Tag not found: {tag_id}")


class TagDuplicateError(DomainError):
    def __init__(self, slug: str) -> None:
        super().__init__(f"Tag with slug '{slug}' already exists")


class TagInactiveError(DomainError):
    def __init__(self, tag_id: int) -> None:
        super().__init__(f"Tag {tag_id} is inactive and cannot be associated")
