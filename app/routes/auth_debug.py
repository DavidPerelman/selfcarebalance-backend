from fastapi import APIRouter
from app.core.security import create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/token/debug")
def get_debug_token(user_id: str):
    token = create_access_token({"sub": user_id})
    return {"access_token": token, "token_type": "bearer"}
