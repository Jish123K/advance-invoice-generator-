import asyncio

import asyncpg

from asyncpg.connection import Connection

from asyncpg.pool import Pool

from asyncpg.exceptions import PostgresError

from pydantic import BaseSettings

class Settings(BaseSettings):

    database_hostname: str

    database_port: str

    database_password: str

    database_name: str

    database_username: str

    class Config:

        env_file = ".env"

settings = Settings()

dsn = f"postgres://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

async def create_pool() -> Pool:

    return await asyncpg.create_pool(dsn=dsn, min_size=1, max_size=5)

async def get_connection(pool: Pool) -> Connection:

    return await pool.acquire()

async def close_connection(connection: Connection) -> None:

    await connection.release()

async def close_pool(pool: Pool) -> None:

    await pool.close()

async def init_db_pool(app) -> None:

    app.pool = await create_pool()

async def close_db_pool(app) -> None:

    await close_pool(app.pool)

async def execute(query, *args):

    async with get_connection(app.pool) as conn:

        try:

            result = await conn.fetch(query, *args)

        except PostgresError as e:

            print(f"Database Error: {e}")

            raise

        return result

async def create_db():

    try:

        await execute("CREATE TABLE IF NOT EXISTS my_table (id SERIAL PRIMARY KEY, name TEXT NOT NULL)")

    except PostgresError as e:

        print(f"Error creating database: {e}")

        raise

async def drop_db():

    try:

        await execute("DROP TABLE IF EXISTS my_table")

    except PostgresError as e:

        print(f"Error dropping database: {e}")

        raise

async def example_query():

    try:

        result = await execute("SELECT * FROM my_table")

        return result

    except PostgresError as e:

        print(f"Error executing query: {e}")

        raise

app = FastAPI(on_startup=[init_db_pool], on_shutdown=[close_db_pool])

@app.post("/create_db")

async def create_db_route():

    await create_db()

    return {"message": "Database created"}

@app.post("/drop_db")

async def drop_db_route():

    await drop_db()

    return {"message": "Database dropped"}

@app.post("/example_query")

async def example_query_route():

    result = await example_query()

    return {"result": result}

