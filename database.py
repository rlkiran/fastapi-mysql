import aiomysql
from fastapi import HTTPException

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "9876543210aA@",
    "db": "item_db"
}

# Function to get database connection
async def get_connection():
    try:
        return await aiomysql.connect(**DB_CONFIG)
    except aiomysql.MySQLError as e:
        raise HTTPException(status_code=500, detail=f"Database connection error: {str(e)}")

# Function to initialize the database
async def init_db():
    try:
        conn = await get_connection()
        async with conn.cursor() as cur:
            # Drop the table if it exists to avoid the warning
            await cur.execute("DROP TABLE IF EXISTS items")
            await conn.commit()

            # Create the table
            await cur.execute("""
                CREATE TABLE IF NOT EXISTS items (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    description TEXT NOT NULL
                )
            """)
            await conn.commit()
        conn.close()
    except aiomysql.MySQLError as e:
        raise HTTPException(status_code=500, detail=f"Error during DB initialization: {str(e)}")

