from fastapi import FastAPI
from contextlib import asynccontextmanager
from database.connectionDB import init_db
from routes.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

# Create the object of FastAPI
app = FastAPI(
    title="Math Microservice with SQLite",
    lifespan=lifespan
)

# This code line defines the existent routes from routes/routes.py
app.include_router(router)
