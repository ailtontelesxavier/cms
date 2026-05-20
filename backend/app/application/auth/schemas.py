from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


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


class UserUpdate(BaseModel):
    name: str | None = None
    is_active: bool | None = None
