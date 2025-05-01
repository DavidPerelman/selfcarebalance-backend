from fastapi import APIRouter, Depends
from app.models.user import User
from app.services.auth import get_current_user
from app.schemas.user import MeResponse

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.get("/me", response_model=MeResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return MeResponse(
        id=str(current_user.id),
        email=current_user.email,
        username=current_user.username,
        full_name=current_user.full_name,
        profile_picture=current_user.profile_picture,
    )
