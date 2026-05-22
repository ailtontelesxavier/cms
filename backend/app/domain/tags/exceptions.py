from app.core.exceptions import DomainError


class TagNotFoundError(DomainError):
    def __init__(self, tag_id: int) -> None:
        super().__init__(f"Tag not found: {tag_id}")


class TagInactiveError(DomainError):
    def __init__(self, tag_id: int) -> None:
        super().__init__(f"Tag {tag_id} is inactive and cannot be associated")
