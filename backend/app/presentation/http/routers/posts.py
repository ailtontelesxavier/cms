from uuid import UUID

from fastapi import APIRouter, Depends

from app.application.posts.schemas import PostCreate, PostDetailOut, PostOut, PostUpdate
from app.application.posts.use_cases import PostUseCases
from app.core.pagination import PaginatedParams, PaginatedResult
from app.domain.auth.entities import User
from app.presentation.http.dependencies import (
    get_post_use_cases,
    require_permission,
)

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("")
async def list_posts(
    page: int = 1,
    page_size: int = 20,
    status: str | None = None,
    q: str | None = None,
    use_cases: PostUseCases = Depends(get_post_use_cases),
) -> PaginatedResult[PostOut]:
    params = PaginatedParams(page=page, page_size=page_size)
    return await use_cases.list_all(params, status=status, q=q)


@router.post("", status_code=201)
async def create_post(
    data: PostCreate,
    current_user: User = Depends(require_permission("posts", "criar")),
    use_cases: PostUseCases = Depends(get_post_use_cases),
) -> PostOut:
    return await use_cases.create(data, current_user.id)


@router.get("/slug/{slug}")
async def get_post_by_slug(
    slug: str,
    use_cases: PostUseCases = Depends(get_post_use_cases),
) -> PostOut:
    return await use_cases.get_by_slug(slug)


@router.get("/{post_id}")
async def get_post(
    post_id: UUID,
    use_cases: PostUseCases = Depends(get_post_use_cases),
) -> PostOut:
    return await use_cases.get_by_id(post_id)


@router.get("/{post_id}/detail")
async def get_post_detail(
    post_id: UUID,
    use_cases: PostUseCases = Depends(get_post_use_cases),
) -> PostDetailOut:
    return await use_cases.get_detail_by_id(post_id)


@router.patch("/{post_id}")
async def update_post(
    post_id: UUID,
    data: PostUpdate,
    _=Depends(require_permission("posts", "atualizar")),
    use_cases: PostUseCases = Depends(get_post_use_cases),
) -> PostOut:
    return await use_cases.update(post_id, data)


@router.post("/{post_id}/publish")
async def publish_post(
    post_id: UUID,
    _=Depends(require_permission("posts", "atualizar")),
    use_cases: PostUseCases = Depends(get_post_use_cases),
) -> PostOut:
    return await use_cases.publish(post_id)


@router.post("/{post_id}/archive")
async def archive_post(
    post_id: UUID,
    _=Depends(require_permission("posts", "atualizar")),
    use_cases: PostUseCases = Depends(get_post_use_cases),
) -> PostOut:
    return await use_cases.archive(post_id)


@router.delete("/{post_id}", status_code=204)
async def delete_post(
    post_id: UUID,
    _=Depends(require_permission("posts", "excluir")),
    use_cases: PostUseCases = Depends(get_post_use_cases),
) -> None:
    await use_cases.delete(post_id)
