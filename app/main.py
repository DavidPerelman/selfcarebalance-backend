from contextlib import asynccontextmanager
from fastapi import APIRouter, Depends, FastAPI
from app.db.init import init_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.routes import mood, auth_debug
import os
import dotenv

dotenv.load_dotenv()

DB_URL = os.getenv("MONGODB_URL")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)

router = APIRouter()


@app.get("/")
def read_root():
    return {"message": "SelfCareBalance API is up!"}


@app.get("/me")
async def read_current_user(user: User = Depends(get_current_user)):
    return {"email": user.email, "id": str(user.id)}


app.include_router(mood.router)
app.include_router(auth_debug.router)
