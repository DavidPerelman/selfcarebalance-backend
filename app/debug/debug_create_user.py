import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import asyncio
from app.models.user import User
from app.db.init import init_db


async def create_user():
    await init_db()  # ודא שהקונפיגורציה נטענת
    user = User(email="test@example.com", username="Test User", is_oauth_user=True)
    await user.insert()
    print("Created user with id:", user.id)


asyncio.run(create_user())
