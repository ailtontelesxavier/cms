from datetime import datetime, timedelta
from uuid import UUID
from zoneinfo import ZoneInfo

from app.application.auth.ports import UserRepository
from app.application.auth.schemas import (
    LoginRequest,
    MFAChallengeRequest,
    MfaInfoOut,
    MFASetupOut,
    MFAVerifyRequest,
    TokenOut,
    UserCreate,
    UserOut,
    UserPasswordUpdate,
    UserUpdate,
)
from app.core.config import settings
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

        return self._issue_tokens(user)

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

        return self._issue_tokens(user)

    async def mfa_challenge(self, data: MFAChallengeRequest) -> TokenOut:
        user = await self.user_repo.get_by_email(data.email)
        if not user or not verify_password(data.password, user.hashed_password):
            raise InvalidCredentialsError()

        if not user.mfa_enabled or not user.totp_secret:
            raise InvalidMFATokenError()

        if not verify_totp(user.totp_secret, data.totp):
            raise InvalidMFATokenError()

        return self._issue_tokens(user)

    async def get_mfa_info(self, user_id: UUID) -> MfaInfoOut:
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise InvalidCredentialsError()

        qrcode = None
        secret = None
        if user.totp_secret:
            secret = user.totp_secret
            uri = get_totp_uri(secret, user.email)
            qrcode = generate_qrcode(uri)

        return MfaInfoOut(
            configured=user.totp_secret is not None,
            enabled=user.mfa_enabled,
            secret=secret,
            qrcode=qrcode,
        )

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

        return self._issue_tokens(user)

    async def verify_user_mfa(self, user_id: UUID, token: str) -> dict:
        user = await self.user_repo.get_by_id(user_id)
        if not user or not user.totp_secret:
            raise InvalidCredentialsError()

        if not verify_totp(user.totp_secret, token):
            raise InvalidMFATokenError()

        user.mfa_enabled = True
        await self.user_repo.update(user)

        return {"detail": "MFA ativado com sucesso"}

    async def create_user(self, data: UserCreate) -> UserOut:
        now = datetime.now(ZoneInfo("America/Sao_Paulo"))
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

    async def list_users(self, params: PaginatedParams, q: str | None = None) -> PaginatedResult[UserOut]:
        users = await self.user_repo.list_all(skip=params.offset, limit=params.limit, q=q)
        total = await self.user_repo.count_all(q=q)
        items = [UserOut.model_validate(u) for u in users]
        return PaginatedResult.create(items, total, params)

    async def update_user(self, user_id: UUID, data: UserUpdate) -> UserOut:
        user = await self.user_repo.get_by_id(user_id)
        datetime.now(ZoneInfo("America/Sao_Paulo"))
        if not user:
            raise InvalidCredentialsError()
        if data.name is not None:
            user.name = data.name
        if data.is_active is not None:
            user.is_active = data.is_active
        user.updated_at = datetime.now(ZoneInfo("America/Sao_Paulo"))
        updated = await self.user_repo.update(user)
        return UserOut.model_validate(updated)

    async def update_user_password(self, user_id: UUID, data: UserPasswordUpdate) -> None:
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise InvalidCredentialsError()
        user.hashed_password = hash_password(data.password)
        user.updated_at = datetime.now(ZoneInfo("America/Sao_Paulo"))
        await self.user_repo.update(user)

    async def delete_user(self, user_id: UUID) -> None:
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise InvalidCredentialsError()
        await self.user_repo.delete(user)

    def _issue_tokens(self, user: User) -> TokenOut:
        access_token = create_token(
            sub=str(user.id),
            email=user.email,
            roles=[r.name for r in user.roles],
            expires_delta=timedelta(minutes=settings.jwt_expiration_minutes),
        )
        refresh_token = create_token(
            sub=str(user.id),
            email=user.email,
            roles=[r.name for r in user.roles],
            expires_delta=timedelta(days=settings.jwt_refresh_expiration_days),
        )
        return TokenOut(access_token=access_token, refresh_token=refresh_token)
