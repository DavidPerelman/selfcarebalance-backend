import os
import httpx
from fastapi import HTTPException
from app.core.config import settings


async def get_google_token(code: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://oauth2.googleapis.com/token",
            data={
                "code": code,
                "client_id": settings.google_client_id,
                "client_secret": settings.google_client_secret,
                "redirect_uri": settings.google_redirect_uri,
                "grant_type": "authorization_code",
            },
        )
    if response.status_code != 200:
        print("Google error:", response.text)
        raise HTTPException(status_code=400, detail="Failed to get token from Google")
    return response.json()


async def get_user_info(access_token: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {access_token}"},
        )
    if response.status_code != 200:
        raise HTTPException(
            status_code=400, detail="Failed to get user info from Google"
        )
    return response.json()
