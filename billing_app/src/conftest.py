import os
import sys

from piccolo.utils.warnings import colored_warning

"""
def pytest_configure(*args):
    if os.environ.get("PICCOLO_TEST_RUNNER") != "True":
        colored_warning(
            "\n\n"
            "We recommend running Piccolo tests using the "
            "`piccolo tester run` command, which wraps Pytest, and makes "
            "sure the test database is being used. "
            "To stop this warning, modify conftest.py."
            "\n\n"
        )
        sys.exit(1)
"""

import asyncio
from dataclasses import dataclass

import aiohttp
import pytest as pytest
from multidict import CIMultiDictProxy
from piccolo.engine import PostgresEngine


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


@pytest.fixture(scope="session")
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture(scope="session")
async def db_client(settings):
    client = PostgresEngine(
        config={
            "database": os.getenv("DB_NAME", "billing_database"),
            "user": os.getenv("DB_USER", "app"),
            "password": os.getenv("DB_PASSWORD", "123qwe"),
            "host": os.getenv("HOST", "localhost"),
            "port": os.getenv("PORT", 5434),
        }
    )
    yield client
    await client.close_connnection_pool()


@pytest.fixture(scope="session")
def settings() -> TestSettings:
    return TestSettings()


@pytest.fixture
def make_get_request(session, settings):
    async def inner(method: str, params: dict = None) -> HTTPResponse:
        params = params or {}
        url = f"http://{settings.service_url}{settings.api_url}{method}"
        async with session.get(url, params=params) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner


@pytest.fixture
def make_post_request(session, settings):
    async def inner(method: str, params: dict = None) -> HTTPResponse:
        params = params or {}
        url = f"http://{settings.service_url}{settings.api_url}{method}"
        async with session.post(url, json=params) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
