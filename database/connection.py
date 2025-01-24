import os
from pymongo import MongoClient
from pymongo.database import Database
from dotenv import load_dotenv
from pathlib import Path


class MongoDB:
    def __init__(self, env_path=None):
        self._load_env(env_path)
        self.uri = os.getenv("URI")
        self.db_name = os.getenv("DB_NAME")
        self.__client__ = None
        self.__db__ = None
        self.connect()

    def _load_env(self, env_path):
        if env_path is None:
            env_path = Path(__file__).parent.parent / ".env"
        if not load_dotenv(dotenv_path=env_path, override=True):
            raise FileNotFoundError(f".env file not found at {env_path}")

    def connect(self):
        if not self.uri:
            raise ValueError("MongoDB URI not found in environment variables.")
        if not self.db_name:
            raise ValueError("Database name not found in environment variables.")

        self.__client__ = MongoClient(self.uri)
        if self.health_check():
            self.__db__ = self.__client__[self.db_name]
        else:
            raise ConnectionError("Database connection failed.")

    @property
    def client(self) -> MongoClient:
        return self.__client__

    @property
    def db(self) -> Database:
        return self.__db__

    def health_check(self) -> bool:
        try:
            self.__client__.admin.command("ping")
            print("Database connection is healthy.")
            return True
        except Exception as e:
            print(f"Database connection is unhealthy: {e}")
            return False
