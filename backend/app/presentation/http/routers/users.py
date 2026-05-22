from uuid import UUID

from fastapi import APIRouter, Depends

from app.application.auth.schemas import MfaInfoOut, MFASetupOut, MFAVerifyRequest, UserCreate, UserOut, UserPasswordUpdate, UserUpdate
from app.application.auth.use_cases import AuthUseCases
from app.core.pagination import PaginatedParams, PaginatedResult
from app.domain.auth.entities import User
from app.presentation.http.dependencies import (
    get_auth_use_cases,
    get_current_user,
    require_permission,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me")
async def get_me(
    current_user: User = Depends(get_current_user),
) -> UserOut:
    return UserOut.model_validate(current_user)


@router.get("")
async def list_users(
    page: int = 1,
    page_size: int = 20,
    q: str | None = None,
    _=Depends(require_permission("auth", "ler")),
    use_cases: AuthUseCases = Depends(get_auth_use_cases),
) -> PaginatedResult[UserOut]:
    params = PaginatedParams(page=page, page_size=page_size)
    return await use_cases.list_users(params, q=q)


@router.post("", status_code=201)
async def create_user(
    data: UserCreate,
    _=Depends(require_permission("auth", "criar")),
    use_cases: AuthUseCases = Depends(get_auth_use_cases),
) -> UserOut:
    return await use_cases.create_user(data)


@router.get("/{user_id}")
async def get_user(
    user_id: UUID,
    _=Depends(require_permission("auth", "ler")),
    use_cases: AuthUseCases = Depends(get_auth_use_cases),
) -> UserOut:
    return await use_cases.get_user(user_id)


@router.patch("/{user_id}")
async def update_user(
    user_id: UUID,
    data: UserUpdate,
    _=Depends(require_permission("auth", "atualizar")),
    use_cases: AuthUseCases = Depends(get_auth_use_cases),
) -> UserOut:
    return await use_cases.update_user(user_id, data)


@router.patch("/{user_id}/password", status_code=204)
async def update_user_password(
    user_id: UUID,
    data: UserPasswordUpdate,
    _=Depends(require_permission("auth", "atualizar")),
    use_cases: AuthUseCases = Depends(get_auth_use_cases),
) -> None:
    await use_cases.update_user_password(user_id, data)


@router.get("/{user_id}/mfa")
async def get_user_mfa(
    user_id: UUID,
    _=Depends(require_permission("auth", "ler")),
    use_cases: AuthUseCases = Depends(get_auth_use_cases),
) -> MfaInfoOut:
    return await use_cases.get_mfa_info(user_id)


@router.post("/{user_id}/mfa/setup")
async def setup_user_mfa(
    user_id: UUID,
    _=Depends(require_permission("auth", "atualizar")),
    use_cases: AuthUseCases = Depends(get_auth_use_cases),
) -> MFASetupOut:
    return await use_cases.setup_mfa(user_id)


@router.post("/{user_id}/mfa/verify")
async def verify_user_mfa(
    user_id: UUID,
    data: MFAVerifyRequest,
    _=Depends(require_permission("auth", "atualizar")),
    use_cases: AuthUseCases = Depends(get_auth_use_cases),
) -> dict:
    return await use_cases.verify_user_mfa(user_id, data.token)


@router.delete("/{user_id}", status_code=204)
async def delete_user(
    user_id: UUID,
    _=Depends(require_permission("auth", "excluir")),
    use_cases: AuthUseCases = Depends(get_auth_use_cases),
) -> None:
    await use_cases.delete_user(user_id)
