from datetime import timedelta
from database.connection import MongoDB
from database.enums import Collections
from faker import Faker
from models import *

faker = Faker(locale=["en_US", "pl_PL"])

# use collections like this: passengers = db.passengers
# then use insert_one or insert_many to insert data like: passengers.insert_one(data)
# or if youre using a model, you can use insert_one or insert_many like this: passengers.insert_one(data.model_dump())


def seed_passengers(db: MongoDB, count: int):
    passengers_collection = db.passengers
    for _ in range(count):
        name: str = faker.first_name()
        surname: str = faker.last_name()
        login: str = faker.user_name()
        password: str = faker.password()
        email: str = faker.email()
        phone: str = "".join(
            str(faker.random_number(1)) for _ in range(faker.random_int(9, 15))
        )
        contact = Contact(email=email, phone=phone if faker.boolean() else None)
        passenger = Passenger(
            name=name, surname=surname, login=login, password=password, contact=contact
        )
        result = passengers_collection.insert_one(passenger.model_dump())


def seed_drivers(db: MongoDB, count: int):
    import uuid

    drivers = db.drivers
    for _ in range(count):
        name: str = faker.first_name()
        surname: str = faker.last_name()
        login: str = faker.user_name()
        password: str = faker.password()
        email: str = faker.email()
        phone: str = "".join(
            str(faker.random_number(1)) for _ in range(faker.random_int(9, 15))
        )
        contact = Contact(email=email, phone=phone if faker.boolean() else None)
        id_license = str(uuid.uuid4())
        issue_date = faker.date_this_century()
        expiration_date = issue_date + timedelta(
            days=365 * faker.random_int(min=5, max=25)
        )
        license = License(
            id_license=id_license, issued_on=issue_date, expires_on=expiration_date
        )
        driver = Driver(
            name=name,
            surname=surname,
            login=login,
            password=password,
            contact=contact,
            license=license,
        )
        result = drivers(driver.model_dump())


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
