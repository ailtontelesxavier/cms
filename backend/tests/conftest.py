import pytest


@pytest.fixture
def mock_db_time():
    """Fixture to freeze time in tests."""


@pytest.fixture
def anyio_backend():
    return "asyncio"
