from fastapi import APIRouter, Depends

from app.application.auth.role_use_cases import RoleUseCases
from app.application.auth.schemas import (
    RoleCreate,
    RoleOut,
    RolePermissionUpdate,
    RoleUpdate,
)
from app.domain.auth.permissions import Acao, Modulo
from app.presentation.http.dependencies import get_role_use_cases, require_permission

router = APIRouter(prefix="/roles", tags=["roles"])


@router.get("")
async def list_roles(
    use_cases: RoleUseCases = Depends(get_role_use_cases),
) -> list[RoleOut]:
    return await use_cases.list_roles()


@router.post("", status_code=201)
async def create_role(
    data: RoleCreate,
    _=Depends(require_permission(Modulo.ADMINISTRATIVO.value, Acao.CRIAR.value)),
    use_cases: RoleUseCases = Depends(get_role_use_cases),
) -> RoleOut:
    return await use_cases.create_role(data)


@router.get("/{role_id}")
async def get_role(
    role_id: int,
    use_cases: RoleUseCases = Depends(get_role_use_cases),
) -> RoleOut:
    return await use_cases.get_role(role_id)


@router.put("/{role_id}")
async def update_role(
    role_id: int,
    data: RoleUpdate,
    _=Depends(require_permission(Modulo.ADMINISTRATIVO.value, Acao.ATUALIZAR.value)),
    use_cases: RoleUseCases = Depends(get_role_use_cases),
) -> RoleOut:
    return await use_cases.update_role(role_id, data)


@router.put("/{role_id}/permissions")
async def update_role_permissions(
    role_id: int,
    data: RolePermissionUpdate,
    _=Depends(require_permission(Modulo.ADMINISTRATIVO.value, Acao.ADMINISTRAR.value)),
    use_cases: RoleUseCases = Depends(get_role_use_cases),
) -> RoleOut:
    return await use_cases.update_role_permissions(role_id, data)


@router.delete("/{role_id}", status_code=204)
async def delete_role(
    role_id: int,
    _=Depends(require_permission(Modulo.ADMINISTRATIVO.value, Acao.EXCLUIR.value)),
    use_cases: RoleUseCases = Depends(get_role_use_cases),
) -> None:
    await use_cases.delete_role(role_id)
