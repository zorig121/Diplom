from motor.motor_asyncio import AsyncIOMotorClient
from core.config import config

db_client = AsyncIOMotorClient(config.MONGO_URI)
database = db_client[config.MONGO_DB_NAME]

async def get_db():
    return database