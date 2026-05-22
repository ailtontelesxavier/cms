from datetime import datetime
from zoneinfo import ZoneInfo

import factory

from app.core.security import hash_password
from app.infrastructure.postgres.models import Post, Role, Tag, User


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session_persistence = "flush"

    email = factory.Sequence(lambda n: f"user{n}@test.com")
    name = factory.Sequence(lambda n: f"User {n}")
    hashed_password = factory.LazyFunction(lambda: hash_password("password123"))
    is_active = True
    is_superuser = False
    mfa_enabled = False
    created_at = factory.LazyFunction(lambda: datetime.now(ZoneInfo("America/Sao_Paulo")))
    updated_at = factory.LazyFunction(lambda: datetime.now(ZoneInfo("America/Sao_Paulo")))


class RoleFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Role
        sqlalchemy_session_persistence = "flush"

    name = factory.Sequence(lambda n: f"Role{n}")
    created_at = factory.LazyFunction(lambda: datetime.now(ZoneInfo("America/Sao_Paulo")))
    updated_at = factory.LazyFunction(lambda: datetime.now(ZoneInfo("America/Sao_Paulo")))


class TagFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Tag
        sqlalchemy_session_persistence = "flush"

    name = factory.Sequence(lambda n: f"Tag {n}")
    is_active = True
    created_at = factory.LazyFunction(lambda: datetime.now(ZoneInfo("America/Sao_Paulo")))
    updated_at = factory.LazyFunction(lambda: datetime.now(ZoneInfo("America/Sao_Paulo")))


class PostFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Post
        sqlalchemy_session_persistence = "flush"

    title = factory.Sequence(lambda n: f"Post {n}")
    slug = factory.Sequence(lambda n: f"post-{n}")
    mongo_object_id = factory.Sequence(lambda n: f"{n:024x}")
    status = "draft"
    created_at = factory.LazyFunction(lambda: datetime.now(ZoneInfo("America/Sao_Paulo")))
    updated_at = factory.LazyFunction(lambda: datetime.now(ZoneInfo("America/Sao_Paulo")))
