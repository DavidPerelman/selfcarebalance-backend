from contextlib import asynccontextmanager
from fastapi import APIRouter, Depends, FastAPI
from app.db.init import init_db
from app.core.dependencies import get_current_user
from app.models.user import User


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()  # 🟢 כאן נבצע אתחול למסד הנתונים
    yield  # המשך הרצת האפליקציה
    # (כאן תוכל לשים קוד לכיבוי אם תרצה בעתיד)


app = FastAPI(lifespan=lifespan)

router = APIRouter()


@app.get("/")
def read_root():
    return {"message": "SelfCareBalance API is up!"}


@app.get("/me")
async def read_current_user(user: User = Depends(get_current_user)):
    return {"email": user.email, "id": str(user.id)}
