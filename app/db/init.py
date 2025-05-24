from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from app.models.user import User
from app.models.mood_entry import MoodEntry
from app.core.config import settings


async def init_db():
    client = AsyncIOMotorClient(settings.mongodb_url)
    database = client.get_default_database()
    await init_beanie(database, document_models=[User, MoodEntry])
