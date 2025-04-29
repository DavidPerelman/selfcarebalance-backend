from fastapi import APIRouter
from app.schemas.user import RegisterRequest
from app.models.user import User
from fastapi import HTTPException, status

router = APIRouter(prefix="/auth", tags=["Auth"])


async def check_user_exists(email: str) -> bool:
    user = await User.find_one(User.email == email)
    return user is not None


@router.post("/register")
async def register_user(user: RegisterRequest):
    if await check_user_exists(user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
