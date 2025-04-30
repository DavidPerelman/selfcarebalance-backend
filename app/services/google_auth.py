import httpx
from fastapi import HTTPException
from app.core.config import settings
from app.models.user import User


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


async def get_or_create_user_from_google_info(google_user_info: dict) -> User:
    user_data = {
        "email": google_user_info["email"],
        "name": google_user_info["name"],
        "picture": google_user_info.get("picture", None),  # אם יש תמונה, אחרת None
    }

    # חיפוש אם המשתמש קיים
    existing_user = await User.find_one({"email": user_data["email"]})
    if existing_user:
        return existing_user  # המשתמש קיים, נחזיר אותו

    # יצירת משתמש חדש
    new_user = User(**user_data)
    await new_user.save()
    return new_user
