import argparse
import asyncio
from datetime import datetime
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings
from app.core.security import hash_password
from app.infrastructure.postgres.models import User


async def create_superuser(email: str, name: str, password: str, roles: list[str] | None = None) -> User | None:
    engine = create_async_engine(settings.database_url)
    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    async with session_factory() as session:
        existing = await session.execute(select(User).where(User.email == email))
        if existing.scalar_one_or_none():
            print(f"User with email '{email}' already exists.")
            return

        now = datetime.now()
        user = User(
            id=uuid4(),
            email=email,
            name=name,
            hashed_password=hash_password(password),
            is_active=True,
            is_superuser=True,
            mfa_enabled=False,
            created_at=now,
            updated_at=now,
        )

        session.add(user)
        await session.flush()
        await session.commit()

        print(f"Superuser created successfully:")
        print(f"  Email:    {email}")
        print(f"  Name:     {name}")
        print(f"  Superuser: True")
        return user


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a superuser for the CMS backend")
    parser.add_argument("--email", required=True, help="User email address")
    parser.add_argument("--name", required=True, help="User display name")
    parser.add_argument("--password", required=True, help="User password")
    args = parser.parse_args()

    asyncio.run(create_superuser(args.email, args.name, args.password))


if __name__ == "__main__":
    main()
