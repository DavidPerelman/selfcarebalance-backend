from fastapi import APIRouter
from fastapi import Depends, HTTPException, status

from app.schemas.user import RegisterRequest, LoginRequest, TokenResponse
from app.models.user import User
from app.services.auth import hash_password, verify_password, create_access_token
from app.schemas.user import UserResponse
from app.services.auth import get_current_user

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


@router.post("/login", response_model=TokenResponse)
async def login_user(data: LoginRequest):
    user = await User.find_one(User.email == data.email)
    if not user:
        raise HTTPException(status_code=400, detail="Email or password error")

    password_correct = verify_password(data.password, user.hashed_password)
    if not password_correct:
        raise HTTPException(status_code=400, detail="Email or password error")

    access_token = create_access_token({"sub": str(user.id)})

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
    )


@router.get("/me")
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user
