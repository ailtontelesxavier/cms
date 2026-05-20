from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID


@dataclass
class User:
    email: str
    name: str
    hashed_password: str
    is_active: bool = True
    is_superuser: bool = False
    mfa_enabled: bool = False
    totp_secret: str | None = None
    id: UUID | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    roles: list["Role"] = field(default_factory=list)


@dataclass
class Role:
    name: str
    description: str | None = None
    id: int | None = None
    permissions: list["Permission"] = field(default_factory=list)


@dataclass
class Permission:
    module: str
    action: str
    id: int | None = None
