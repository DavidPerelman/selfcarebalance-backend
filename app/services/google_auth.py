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


async def get_or_create_user_from_google_info(user_info: dict) -> User:
    print(f"Received user info: {user_info}")

    # בדוק אם המשתמש קיים
    user = await User.find_one({"email": user_info["email"].lower().strip()})
    if user:
        print(f"User found: {user_info['email']}")
        return user

    # יצירת משתמש חדש אם לא נמצא
    user_data = {
        "email": user_info["email"],
        "username": user_info["email"],  # או שם מלא אם תרצה
        "full_name": user_info.get("name"),
        "profile_picture": user_info.get("picture"),
        "is_oauth_user": True,
    }

    print(f"Creating new user with data: {user_data}")
    new_user = User(**user_data)
    await new_user.insert()
    print(f"New user created: {new_user.email}")
    return new_user
