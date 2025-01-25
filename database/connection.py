import os
from typing import List
from pymongo.collection import Collection
from pymongo import MongoClient
from pymongo.database import Database
from dotenv import load_dotenv
from pathlib import Path
from .enums import Collections


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

    def clear_database(self, collections: List[Collections] = None) -> None:
        """
        Clear all documents from specified collections. If no collections are specified, all collections will be cleared.
        """
        if not collections:
            collections = self.__db__.list_collection_names()
        else:
            collections = [collection.value for collection in collections]
        for collection_name in collection:
            collection = self.__db__.get_collection(collection_name)
            deleted_count = collection.delete_many({}).deleted_count
            print(
                f"Cleared {deleted_count} documents from collection '{collection_name}'."
            )

    def health_check(self) -> bool:
        try:
            self.__client__.admin.command("ping")
            print("Database connection is healthy.")
            return True
        except Exception as e:
            print(f"Database connection is unhealthy: {e}")
            return False

    def __get_collection__(self, collection: Collections):
        if collection not in self.__db__.list_collection_names():
            return self.__db__.create_collection(collection)
        return self.__db__.get_collection(collection)

    @property
    def passengers(self) -> Collection:
        return self.__get_collection__(Collections.PASSENGERS)

    @property
    def drivers(self) -> Collection:
        return self.__get_collection__(Collections.DRIVERS)

    @property
    def editors(self) -> Collection:
        return self.__get_collection__(Collections.EDITORS)

    @property
    def inspectors(self) -> Collection:
        return self.__get_collection__(Collections.INSPECTORS)

    @property
    def vehicles(self) -> Collection:
        return self.__get_collection__(Collections.VEHICLES)

    @property
    def lines(self) -> Collection:
        return self.__get_collection__(Collections.LINES)

    @property
    def rides(self) -> Collection:
        return self.__get_collection__(Collections.RIDES)

    @property
    def stops(self) -> Collection:
        return self.__get_collection__(Collections.STOPS)

    @property
    def ticket_types(self) -> Collection:
        return self.__get_collection__(Collections.TICKET_TYPES)

    @property
    def tickets(self) -> Collection:
        return self.__get_collection__(Collections.TICKETS)

    @property
    def fines(self) -> Collection:
        return self.__get_collection__(Collections.FINES)

    @property
    def inspections(self) -> Collection:
        return self.__get_collection__(Collections.INSPECTIONS)
