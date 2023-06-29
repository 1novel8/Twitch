from envparse import Env
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseSettings


class Settings(BaseSettings):
    server_host: str = "0.0.0.1"
    server_port: int = 8080


settings = Settings(
    _env_file='.env',
    _env_file_encoding='utf-8',
)


env = Env()
MONGODB_URL = env.str("MONGODB_URL", default="mongodb://localhost:27017/twitch_db")

client = AsyncIOMotorClient(MONGODB_URL)

db = client.twitch_db
user_collection = db.users
stream_collection = db.streams
