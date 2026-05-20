from app.core.exceptions import DomainError


class PostNotFoundError(DomainError):
    def __init__(self, post_id: str) -> None:
        super().__init__(f"Post not found: {post_id}")


class PostSlugDuplicateError(DomainError):
    def __init__(self, slug: str) -> None:
        super().__init__(f"Post with slug '{slug}' already exists")


class InvalidStatusTransitionError(DomainError):
    def __init__(self, current: str, target: str) -> None:
        super().__init__(f"Cannot transition from '{current}' to '{target}'")


class PostContentMissingError(DomainError):
    def __init__(self) -> None:
        super().__init__("Post has no HTML content in MongoDB")
