import os
import httpx
from jose import jwt
from app.core.config import settings
from fastapi import APIRouter, Request
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


@router.get("/callback")
async def google_callback(request: Request):
    code = request.query_params.get("code")
    if not code:
        return {"error": "No code provided"}

    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": settings.google_client_id,
        "client_secret": settings.google_client_secret,
        "redirect_uri": settings.google_redirect_uri,
        "grant_type": "authorization_code",
    }

    async with httpx.AsyncClient() as client:
        token_response = await client.post(token_url, data=data)
        token_json = token_response.json()

    id_token = token_json.get("id_token")
    if not id_token:
        return {"error": "No id_token returned"}

    decoded_token = jwt.get_unverified_claims(id_token)
    email = decoded_token.get("email")
    name = decoded_token.get("name")
    picture = decoded_token.get("picture")

    return {"email": email, "name": name, "picture": picture}
