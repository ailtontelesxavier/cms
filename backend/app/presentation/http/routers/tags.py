from fastapi import APIRouter, Depends

from app.application.tags.schemas import TagCreate, TagOut, TagUpdate
from app.application.tags.use_cases import TagUseCases
from app.core.pagination import PaginatedParams, PaginatedResult
from app.presentation.http.dependencies import get_tag_use_cases, require_permission

router = APIRouter(prefix="/tags", tags=["tags"])


@router.get("")
async def list_tags(
    page: int = 1,
    page_size: int = 20,
    use_cases: TagUseCases = Depends(get_tag_use_cases),
) -> PaginatedResult[TagOut]:
    params = PaginatedParams(page=page, page_size=page_size)
    return await use_cases.list_all(params)


@router.post("", status_code=201)
async def create_tag(
    data: TagCreate,
    _=Depends(require_permission("tags", "criar")),
    use_cases: TagUseCases = Depends(get_tag_use_cases),
) -> TagOut:
    return await use_cases.create(data)


@router.get("/{tag_id}")
async def get_tag(
    tag_id: int,
    use_cases: TagUseCases = Depends(get_tag_use_cases),
) -> TagOut:
    return await use_cases.get_by_id(tag_id)


@router.patch("/{tag_id}")
async def update_tag(
    tag_id: int,
    data: TagUpdate,
    _=Depends(require_permission("tags", "atualizar")),
    use_cases: TagUseCases = Depends(get_tag_use_cases),
) -> TagOut:
    return await use_cases.update(tag_id, data)


@router.delete("/{tag_id}", status_code=204)
async def delete_tag(
    tag_id: int,
    _=Depends(require_permission("tags", "excluir")),
    use_cases: TagUseCases = Depends(get_tag_use_cases),
) -> None:
    await use_cases.delete(tag_id)
