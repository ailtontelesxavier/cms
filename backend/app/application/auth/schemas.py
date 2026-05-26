from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, field_validator

from app.domain.auth.permissions import Acao, Modulo


class LoginRequest(BaseModel):
    email: str = Field(..., max_length=255)
    password: str = Field(..., min_length=1)


class TokenOut(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    refresh_token: str


class MFAVerifyRequest(BaseModel):
    token: str = Field(..., min_length=6, max_length=6)


class MFAChallengeRequest(BaseModel):
    email: str = Field(..., max_length=255)
    password: str = Field(..., min_length=1)
    totp: str = Field(..., min_length=6, max_length=6)


class MfaInfoOut(BaseModel):
    configured: bool
    enabled: bool
    secret: str | None = None
    qrcode: str | None = None


class MFASetupOut(BaseModel):
    secret: str
    qrcode: str


class UserCreate(BaseModel):
    email: str = Field(..., max_length=255)
    name: str = Field(..., min_length=1, max_length=255)
    password: str = Field(..., min_length=8)


class UserOut(BaseModel):
    id: UUID
    email: str
    name: str
    is_active: bool
    is_superuser: bool
    mfa_enabled: bool
    created_at: datetime
    updated_at: datetime
    roles: list[str] = []

    model_config = {"from_attributes": True}

    @field_validator("roles", mode="before")
    @classmethod
    def coerce_roles(cls, v: object) -> list[str]:
        if isinstance(v, list):
            return [r.name if hasattr(r, "name") else str(r) for r in v]
        return v if isinstance(v, list) else []


class UserUpdate(BaseModel):
    name: str | None = None
    is_active: bool | None = None


class UserPasswordUpdate(BaseModel):
    password: str = Field(..., min_length=8)


class PermissionOut(BaseModel):
    id: int
    module: str
    action: str

    model_config = {"from_attributes": True}


class RoleCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str | None = None


class RoleUpdate(BaseModel):
    name: str | None = None
    description: str | None = None


class PermissionCreate(BaseModel):
    module: Modulo
    action: Acao


class RolePermissionUpdate(BaseModel):
    permissions: list[PermissionCreate]


class RoleOut(BaseModel):
    id: int
    name: str
    description: str | None = None
    permissions: list[PermissionOut] = []

    model_config = {"from_attributes": True}


class UserRoleAssign(BaseModel):
    role_ids: list[int]
