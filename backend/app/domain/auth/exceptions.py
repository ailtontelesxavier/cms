from app.core.exceptions import ForbiddenError, UnauthorizedError


class InvalidCredentialsError(UnauthorizedError):
    def __init__(self) -> None:
        super().__init__("Invalid credentials")


class MFASetupRequiredError(UnauthorizedError):
    def __init__(self) -> None:
        super().__init__("MFA token required")


class InvalidMFATokenError(UnauthorizedError):
    def __init__(self) -> None:
        super().__init__("Invalid MFA token")


class PermissionDeniedError(ForbiddenError):
    def __init__(self, module: str, action: str) -> None:
        super().__init__(f"Permission denied: {module}:{action}")
