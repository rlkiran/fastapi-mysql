from fastapi import FastAPI
from routes.item_routes import item_routes
from database import init_db

async def lifespan(app: FastAPI):
    # Initialization logic on startup
    await init_db()
    yield
    # Cleanup logic on shutdown (if needed)

app = FastAPI(lifespan=lifespan)

app.include_router(item_routes)
