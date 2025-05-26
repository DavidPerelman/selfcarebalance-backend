import os
from fastapi import APIRouter
from fastapi.responses import RedirectResponse

router = APIRouter(prefix="/auth/google", tags=["auth-google"])


@router.get("/login")
def login_with_google():
    base_url = "https://accounts.google.com/o/oauth2/v2/auth"
    client_id = os.getenv("GOOGLE_CLIENT_ID")
    redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")
    scope = "openid email profile"
    response_type = "code"
    access_type = "offline"
    prompt = "consent"

    url = (
        f"{base_url}?"
        f"response_type={response_type}&"
        f"client_id={client_id}&"
        f"redirect_uri={redirect_uri}&"
        f"scope={scope}&"
        f"access_type={access_type}&"
        f"prompt={prompt}"
    )

    return RedirectResponse(url)
