from fastapi import FastAPI
from routes.item_routes import item_routes
from fastapi.middleware.cors import CORSMiddleware
from database import init_db

async def lifespan(app: FastAPI):
    # Initialization logic on startup
    await init_db()
    yield
    # Cleanup logic on shutdown (if needed)

app = FastAPI(lifespan=lifespan)
# Allow all origins (change this to specific origins if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can replace "*" with ["http://127.0.0.1:5500"]
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers
)
app.include_router(item_routes)
