import os
from typing import Any

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()


class DatabaseClient:
    _client: MongoClient | None = None

    @classmethod
    def get_client(cls) -> MongoClient | None:
        if cls._client is not None:
            return cls._client

        mongo_uri = os.getenv('MONGODB_URI') or os.getenv('MONGO_URI')
        if not mongo_uri:
            return None

        try:
            cls._client = MongoClient(mongo_uri, serverSelectionTimeoutMS=2000)
            cls._client.admin.command('ping')
            return cls._client
        except Exception:
            return None

    @classmethod
    def get_db(cls) -> Any:
        client = cls.get_client()
        if client is None:
            return None
        return client[os.getenv('MONGODB_DATABASE') or os.getenv('DATABASE_NAME', 'logimind')]


def get_database() -> Any:
    return DatabaseClient.get_db()
