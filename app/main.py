from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.db.init import init_db


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
