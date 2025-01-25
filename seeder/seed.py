from database.connection import MongoDB
from database.enums import Collections
from faker import Faker
from models import *

faker = Faker(locale=["en_US", "pl_PL"])

# use collections like this: passengers = db.passengers
# then use insert_one or insert_many to insert data like: passengers.insert_one(data)
# or if youre using a model, you can use insert_one or insert_many like this: passengers.insert_one(data.model_dump())


def seed_passengers(db: MongoDB, count: int):
    passengers = db.passengers
    raise NotImplementedError


def seed_drivers(db: MongoDB, count: int):
    editors = db.editors
    raise NotImplementedError


def seed_editors(db: MongoDB, count: int):
    raise NotImplementedError


def seed_inspectors(db: MongoDB, count: int):
    raise NotImplementedError


def seed_vehicles(db: MongoDB, count: int):
    raise NotImplementedError


def seed_lines(db: MongoDB, count: int):
    raise NotImplementedError


def seed_rides(db: MongoDB, count: int):
    raise NotImplementedError


def seed_stops(db: MongoDB, count: int):
    raise NotImplementedError


def seed_ticket_types(db: MongoDB, count: int):
    raise NotImplementedError


def seed_tickets(db: MongoDB, count: int):
    raise NotImplementedError


def seed_fines(db: MongoDB, count: int):
    raise NotImplementedError


def seed_inspections(db: MongoDB, count: int):
    raise NotImplementedError
