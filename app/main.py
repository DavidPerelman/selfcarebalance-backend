import os
from starlette.middleware.sessions import SessionMiddleware
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.db.init import init_db
from app.routes.auth import router as auth_router
from app.routes.mood import router as mood_router
from app.routes.auth_google import router as google_auth_router
from app.routes.auth_info import router as auth_info_router

from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()  # כאן מתחבר ל־MongoDB
    yield  # כאן מתחיל השרת
    # אפשר להוסיף כאן קוד סגירה (אם צריך בעתיד)


app = FastAPI(
    title="SelfCareBalance API",
    description="מצא את האיזון שבך | Find your inner balance",
    version="0.1.0",
    lifespan=lifespan,  # כאן עובר הפונקציה
)


@app.get("/")
async def root():
    return {"message": "Welcome to SelfCareBalance API!"}


app.add_middleware(
    SessionMiddleware, secret_key=settings.secret_key  # או settings.secret_key
)

app.include_router(auth_router)
app.include_router(mood_router)
app.include_router(google_auth_router)
app.include_router(auth_info_router)
