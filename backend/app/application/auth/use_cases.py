from datetime import datetime
from uuid import UUID

from app.application.auth.ports import UserRepository
from app.application.auth.schemas import (
    LoginRequest,
    MFASetupOut,
    MFAVerifyRequest,
    TokenOut,
    UserCreate,
    UserOut,
)
from app.core.pagination import PaginatedParams, PaginatedResult
from app.core.security import (
    create_token,
    decode_token,
    generate_qrcode,
    generate_totp_secret,
    get_totp_uri,
    hash_password,
    verify_password,
    verify_totp,
)
from app.domain.auth.entities import User
from app.domain.auth.exceptions import (
    InvalidCredentialsError,
    InvalidMFATokenError,
    PermissionDeniedError,
)


class AuthUseCases:
    def __init__(self, user_repo: UserRepository) -> None:
        self.user_repo = user_repo

    async def login(self, data: LoginRequest) -> TokenOut:
        user = await self.user_repo.get_by_email(data.email)
        if not user or not verify_password(data.password, user.hashed_password):
            raise InvalidCredentialsError()

        if user.mfa_enabled:
            raise PermissionDeniedError("auth", "mfa_required")

        token = create_token(
            sub=str(user.id),
            email=user.email,
            roles=[r.name for r in user.roles],
        )
        return TokenOut(access_token=token)

    async def refresh(self, refresh_token: str) -> TokenOut:
        try:
            payload = decode_token(refresh_token)
        except Exception:
            raise InvalidCredentialsError() from None

        user_id = payload.get("sub")
        if not user_id:
            raise InvalidCredentialsError()

        user = await self.user_repo.get_by_id(UUID(user_id))
        if not user or not user.is_active:
            raise InvalidCredentialsError()

        token = create_token(
            sub=str(user.id),
            email=user.email,
            roles=[r.name for r in user.roles],
        )
        return TokenOut(access_token=token)

    async def setup_mfa(self, user_id: UUID) -> MFASetupOut:
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise InvalidCredentialsError()

        secret = generate_totp_secret()
        user.totp_secret = secret
        user.mfa_enabled = False
        await self.user_repo.update(user)

        uri = get_totp_uri(secret, user.email)
        qrcode_svg = generate_qrcode(uri)
        return MFASetupOut(secret=secret, qrcode=qrcode_svg)

    async def verify_mfa(self, user_id: UUID, data: MFAVerifyRequest) -> TokenOut:
        user = await self.user_repo.get_by_id(user_id)
        if not user or not user.totp_secret:
            raise InvalidCredentialsError()

        if not verify_totp(user.totp_secret, data.token):
            raise InvalidMFATokenError()

        user.mfa_enabled = True
        await self.user_repo.update(user)

        token = create_token(
            sub=str(user.id),
            email=user.email,
            roles=[r.name for r in user.roles],
        )
        return TokenOut(access_token=token)

    async def create_user(self, data: UserCreate) -> UserOut:
        now = datetime.utcnow()
        user = User(
            email=data.email,
            name=data.name,
            hashed_password=hash_password(data.password),
            created_at=now,
            updated_at=now,
        )
        created = await self.user_repo.create(user)
        return UserOut.model_validate(created)

    async def get_user(self, user_id: UUID) -> UserOut:
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise InvalidCredentialsError()
        return UserOut.model_validate(user)

    async def list_users(self, params: PaginatedParams) -> PaginatedResult[UserOut]:
        users = await self.user_repo.list_all(skip=params.offset, limit=params.limit)
        total = await self.user_repo.count_all()
        items = [UserOut.model_validate(u) for u in users]
        return PaginatedResult.create(items, total, params)
