import os
from beanie import init_beanie
import dotenv
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from .models.user import User

dotenv.load_dotenv()

DB_URL = os.getenv("MONGODB_URL")

app = FastAPI()


@app.on_event("startup")
async def connect_to_db():
    client = AsyncIOMotorClient(DB_URL)
    await init_beanie(client.get_database(), document_models=[User])


@app.get("/")
def read_root():
    return {"message": "SelfCareBalance API is up!"}
