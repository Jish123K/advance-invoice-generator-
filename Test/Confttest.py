import asyncio

import asyncpg

import pytest

from fastapi import FastAPI

from fastapi.testclient import TestClient

app = FastAPI()

@app.on_event("startup")

async def startup():

    app.db_pool = await asyncpg.create_pool(

        user="user",

        password="password",

        database="database",

        host="localhost"

    )

@app.on_event("shutdown")

async def shutdown():

    await app.db_pool.close()

async def create_user(username, email, password):

    async with app.db_pool.acquire() as conn:

        user_id = await conn.fetchval(

            "INSERT INTO users (username, email, password) VALUES ($1, $2, $3) RETURNING id",

            username, email, password

        )

        return user_id

async def create_product(product_name, quantity_init, quantity_left):

    async with app.db_pool.acquire() as conn:

        product_id = await conn.fetchval(

            "INSERT INTO products (product_name, quantity_init, quantity_left) VALUES ($1, $2, $3) RETURNING id",

            product_name, quantity_init, quantity_left

        )

        return product_id

async def create_invoice(user_id, reference, value_net, actual_payment, items):

    async with app.db_pool.acquire() as conn:

        async with conn.transaction():

            invoice_id = await conn.fetchval(

                "INSERT INTO invoices (invoice_owner_id, reference, value_net, actual_payment, payment_due) VALUES ($1, $2, $3, $4, $5) RETURNING id",

                user_id, reference, value_net, actual_payment, (value_net - actual_payment)

            )

            for item in items:

                await conn.execute(

                    "INSERT INTO invoice_items (invoice_id, product_name, quantity, prix_unit) VALUES ($1, $2, $3, $4)",

                    invoice_id, item["product_name"], item["quantity"], item["prix_unit"]

                )

            return invoice_id

@pytest.fixture

async def client():

    async with TestClient(app) as client:

        yield client

@pytest.fixture

async def db():

    db_pool = await asyncpg.create_pool(

        user="user",

        password="password",

        database="database_test",

        host="localhost"

    )

    yield db_pool

    await db_pool.close()

@pytest.fixture

async def test_user(db):

    user_id = await create_user("thiere", "thiern@gmail.com", "thierno")

    return {"id": user_id, "username": "thiere", "email": "thiern@gmail.com", "password": "thierno"}

@pytest.fixture

async def token(test_user):

    # Implement token generation here

    pass

@pytest.fixture

async def authorized_client(client, token):

    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}

    return client

@pytest.fixture

": 123, "quantity_left": 13},
async def test_products(db):

products = [

{"product_name": "sac a dos", "quantity_init": 122, "quantity_left": 123},

{"product_name": "chaussure", "quantity_init": 150, "quantity_left": 133},

{"product_name": "savon", "quantity_init": 133, "quantity_left": 100},

{"product_name": "citron", "quantity_init": 190, "quantity_left": 190},

{"product_name": "sauce", "quantity_init": 123, "quantity_left": 13},

]

product_records = []
    
async with db.transaction():

    for product in products:

        query = products_table.insert().values(

            product_name=product['product_name'],

            quantity_init=product['quantity_init'],

            quantity_left=product['quantity_left']

        )

        product_record = await db.fetch_one(query)

        product_records.append(product_record)

return product_records



