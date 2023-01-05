import asyncio
from dataclasses import dataclass

import aiohttp
import pytest as pytest
from multidict import CIMultiDictProxy
from piccolo.engine import PostgresEngine

from .settings import TestSettings


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
            "database": "billing_database",
            "user": "app",
            "password": "123qwe",
            "host": "localhost",
            "port": 5434,
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
