from fastapi import APIRouter, Request
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from fastapi.responses import RedirectResponse

from app.services.google_auth import (
    get_google_token,
    get_user_info,
    get_or_create_user_from_google_info,
)
from app.core.config import settings
from app.models.user import User
from app.services.auth import create_access_token

router = APIRouter(prefix="/auth", tags=["Auth - Google"])

# טוען משתני סביבה
config = Config(".env")

oauth = OAuth(config)

oauth.register(
    name="google",
    client_id=settings.google_client_id,
    client_secret=settings.google_client_secret,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)


@router.get("/google/login")
async def login_via_google(request: Request):
    redirect_uri = settings.google_redirect_uri
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/google/callback")
async def login_via_google(code: str):  # noqa: F811
    token_data = await get_google_token(code)
    access_token = token_data["access_token"]

    user_info = await get_user_info(access_token)

    # שמירה או יצירת משתמש ב־MongoDB
    user = await get_or_create_user_from_google_info(user_info)

    jwt_token = create_access_token({"sub": str(user.id)})

    redirect_url = f"{settings.frontend_url}/auth/google/callback?token={jwt_token}"

    return RedirectResponse(redirect_url)
