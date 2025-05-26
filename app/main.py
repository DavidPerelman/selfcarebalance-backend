from contextlib import asynccontextmanager
from fastapi import APIRouter, Depends, FastAPI
from app.db.init import init_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.routes import mood, auth_debug
import os
from beanie import init_beanie
import dotenv
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from .models.user import User

dotenv.load_dotenv()

DB_URL = os.getenv("MONGODB_URL")

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()  # 🟢 כאן נבצע אתחול למסד הנתונים
    yield  # המשך הרצת האפליקציה
    # (כאן תוכל לשים קוד לכיבוי אם תרצה בעתיד)


app = FastAPI(lifespan=lifespan)

router = APIRouter()


@app.on_event("startup")
async def connect_to_db():
    client = AsyncIOMotorClient(DB_URL)
    await init_beanie(client.get_database(), document_models=[User])


@app.get("/")
def read_root():
    return {"message": "SelfCareBalance API is up!"}


@app.get("/me")
async def read_current_user(user: User = Depends(get_current_user)):
    return {"email": user.email, "id": str(user.id)}


app.include_router(mood.router)
app.include_router(auth_debug.router)
