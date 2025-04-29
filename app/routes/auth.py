from fastapi import APIRouter
from fastapi import HTTPException, status

from app.schemas.user import RegisterRequest
from app.models.user import User
from app.services.auth import hash_password
from app.schemas.user import UserResponse

router = APIRouter(prefix="/auth", tags=["Auth"])


async def check_user_exists(email: str) -> bool:
    user = await User.find_one(User.email == email)
    return user is not None


@router.post("/register")
async def register_user(user: RegisterRequest):
    if await check_user_exists(user.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = hash_password(user.password)

    new_user = User(username=user.username, email=user.email, hashed_password=hashed)

    await new_user.insert()

    return UserResponse(
        id=str(new_user.id),
        username=new_user.username,
        email=new_user.email,
        created_at=new_user.created_at,
    )
