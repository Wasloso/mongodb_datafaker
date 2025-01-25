from database.connection import MongoDB
from database.enums import Collections
from faker import Faker
from models import *
from pymongo.database import Database


def seed_passengers(db: Database, count: int):
    raise NotImplementedError


def seed_drivers(db: Database, count: int):
    raise NotImplementedError


def seed_editors(db: Database, count: int):
    raise NotImplementedError


def seed_inspectors(db: Database, count: int):
    raise NotImplementedError


def seed_vehicles(db: Database, count: int):
    raise NotImplementedError


def seed_lines(db: Database, count: int):
    raise NotImplementedError


def seed_rides(db: Database, count: int):
    raise NotImplementedError


def seed_stops(db: Database, count: int):
    raise NotImplementedError


def seed_ticket_types(db: Database, count: int):
    raise NotImplementedError


def seed_tickets(db: Database, count: int):
    raise NotImplementedError


def seed_fines(db: Database, count: int):
    raise NotImplementedError


def seed_inspections(db: Database, count: int):
    raise NotImplementedError


def __check_collection(db: Database, collection: Collections):
    if collection not in db.list_collection_names():
        print(f"Collection {collection} not found. Creating collection.")
        db.create_collection(collection)
