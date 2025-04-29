from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.db.init import init_db
from app.routes.auth import router as auth_router
from app.routes.mood import router as mood_router


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


app.include_router(auth_router)
app.include_router(mood_router)
