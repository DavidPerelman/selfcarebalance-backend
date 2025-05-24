from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db.init import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()  # כאן מתחבר ל־MongoDB
    yield  # כאן מתחיל השרת
    # אפשר להוסיף כאן קוד סגירה (אם צריך בעתיד)


app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "SelfCareBalance API is up!"}
