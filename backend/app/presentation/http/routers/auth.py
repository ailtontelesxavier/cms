from fastapi import APIRouter, Depends

from app.application.auth.schemas import (
    LoginRequest,
    MFASetupOut,
    MFAVerifyRequest,
    RefreshRequest,
    TokenOut,
)
from app.application.auth.use_cases import AuthUseCases
from app.domain.auth.entities import User
from app.presentation.http.dependencies import get_auth_use_cases, get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token")
async def login(
    data: LoginRequest,
    use_cases: AuthUseCases = Depends(get_auth_use_cases),
) -> TokenOut:
    return await use_cases.login(data)


@router.post("/refresh")
async def refresh(
    data: RefreshRequest,
    use_cases: AuthUseCases = Depends(get_auth_use_cases),
) -> TokenOut:
    return await use_cases.refresh(data.refresh_token)


@router.post("/mfa/setup")
async def setup_mfa(
    current_user: User = Depends(get_current_user),
    use_cases: AuthUseCases = Depends(get_auth_use_cases),
) -> MFASetupOut:
    return await use_cases.setup_mfa(current_user.id)


@router.post("/mfa/verify")
async def verify_mfa(
    data: MFAVerifyRequest,
    current_user: User = Depends(get_current_user),
    use_cases: AuthUseCases = Depends(get_auth_use_cases),
) -> TokenOut:
    return await use_cases.verify_mfa(current_user.id, data)
