import aiomysql
from fastapi import FastAPI

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "9876543210aA@",
    "db": "item_db"
}

async def get_connection():
    return await aiomysql.connect(**DB_CONFIG)

async def init_db():
    conn = await get_connection()
    async with conn.cursor() as cur:
        await cur.execute("""
            CREATE TABLE IF NOT EXISTS items (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                description TEXT NOT NULL
            )
        """)
        await conn.commit()
    conn.close()
