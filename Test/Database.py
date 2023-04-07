import asyncio

import pytest

import asyncpg

from asyncpg.pool import Pool

from asyncpg.exceptions import UniqueViolationError

from fastapi import FastAPI

from httpx import AsyncClient

from app.config import settings

from app.database import Base, get_database_url, get_pool

@pytest.fixture(scope='session')

async def database_pool() -> Pool:

    pool = await asyncpg.create_pool(

        get_database_url(),

        min_size=2,

        max_size=10

    )

    yield pool

    await pool.close()

@pytest.fixture(scope='session')

def event_loop():

    loop = asyncio.get_event_loop_policy().new_event_loop()

    yield loop

    loop.close()

@pytest.fixture()

async def database(database_pool):

    await database_pool.execute('DROP SCHEMA public CASCADE')

    await database_pool.execute('CREATE SCHEMA public')

    async with database_pool.acquire() as conn:

        async with conn.transaction():

            await conn.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')

            await conn.execute(Base.metadata.create_all(conn))

            yield conn

            await conn.execute('ROLLBACK')

@pytest.fixture()

async def client(database_pool):

    app = FastAPI()

    app.dependency_overrides[get_pool] = lambda: database_pool

    @app.exception_handler(UniqueViolationError)

    async def unique_violation_exception_handler(request, exc):

        return JSONResponse(status_code=409, content={"detail": str(exc)})

    async with AsyncClient(app=app, base_url='http://test') as client:

        yield client

