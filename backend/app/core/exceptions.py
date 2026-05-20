class DomainError(Exception):
    """Base exception for domain errors."""


class NotFoundError(DomainError):
    def __init__(self, resource: str, resource_id: str) -> None:
        self.resource = resource
        self.resource_id = resource_id
        super().__init__(f"{resource} not found: {resource_id}")


class DuplicateError(DomainError):
    def __init__(self, resource: str, field: str, value: str) -> None:
        self.resource = resource
        self.field = field
        self.value = value
        super().__init__(f"{resource} with {field} '{value}' already exists")


class UnauthorizedError(DomainError):
    def __init__(self, message: str = "Unauthorized") -> None:
        super().__init__(message)


class ForbiddenError(DomainError):
    def __init__(self, message: str = "Forbidden") -> None:
        super().__init__(message)


class ValidationError(DomainError):
    def __init__(self, message: str) -> None:
        super().__init__(message)
