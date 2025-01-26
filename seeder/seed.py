from datetime import timedelta
from typing import List, Tuple
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
    total_added = 0
    for i in range(count):
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
        if result.acknowledged:
            total_added += 1
        printProgressBar(i + 1, count, length=50, prefix="passengers")


def seed_drivers(db: MongoDB, count: int):
    import uuid

    drivers = db.drivers
    total_added = 0
    for i in range(count):
        name, surname, login, password, contact = __generate_user_data()
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
        result = drivers.insert_one(driver.model_dump())
        if result.acknowledged:
            total_added += 1
        printProgressBar(i + 1, count, length=50, prefix="drivers")


def seed_editors(db: MongoDB, count: int):
    editors_collection = db.editors
    total_added = 0
    for i in range(count):
        name, surname, login, password, contact = __generate_user_data()
        editor = Editor(
            name=name, surname=surname, login=login, password=password, contact=contact
        )
        result = editors_collection.insert_one(editor.model_dump())
        if result.acknowledged:
            total_added += 1
        printProgressBar(i + 1, count, length=50, prefix="editors")


def seed_inspectors(db: MongoDB, count: int):
    inspectors_collection = db.inspectors
    total_added = 0
    for i in range(count):
        name, surname, login, password, contact = __generate_user_data()
        inspector = Inspector(
            name=name, surname=surname, login=login, password=password, contact=contact
        )
        result = inspectors_collection.insert_one(inspector.model_dump())
        if result.acknowledged:
            total_added += 1
        printProgressBar(i + 1, count, length=50, prefix="inspectors")


def seed_vehicles(db: MongoDB, count: int):
    vehicles_collection = db.vehicles
    existing_numbers = set(vehicles_collection.distinct("number"))
    total_added = 0
    for i in range(count):
        while (number := faker.license_plate()) in existing_numbers:
            pass
        capacity = faker.random_int(min=10, max=250)
        production_date = faker.date_this_century()
        vehicle_type = faker.random_element(VehicleType).value
        air_conditioning = faker.boolean(chance_of_getting_true=70)
        status = faker.random_element(VehicleStatus).value
        vehicle = Vehicle(
            number=number,
            capacity=capacity,
            production_date=production_date,
            vehicle_type=vehicle_type,
            air_conditioning=air_conditioning,
            type=vehicle_type,
            status=status,
        )
        result = vehicles_collection.insert_one(vehicle.model_dump())
        if result.acknowledged:
            total_added += 1
        printProgressBar(i + 1, count, length=50, prefix="vehicles")


def seed_lines(db: MongoDB, count: int):
    lines_collection = db.lines
    existing_numbers = set(lines_collection.distinct("number"))
    stops = [Stop(**stop) for stop in db.stops.find()]
    if not stops or len(stops) < 2:
        print("Not enough stops to seed lines, skipping")
        return
    total_added = 0
    for i in range(count):
        while (
            number := str(faker.random_int(min=0, max=1000))
            + (
                faker.random_letter()
                if faker.boolean(chance_of_getting_true=10)
                else ""
            )
        ) in existing_numbers:
            pass
        existing_numbers.add(number)
        path = __generate_path(stops)
        line = Line(number=number, path=path)
        result = lines_collection.insert_one(line.model_dump())
        if result.acknowledged:
            total_added += 1
        printProgressBar(i + 1, count, length=50, prefix="lines")


def seed_rides(db: MongoDB, count: int):
    raise NotImplementedError("Rides model not implemented yet")
    rides_collection = db.rides
    vehicles_ids = db.vehicles.distinct("_id")
    if not vehicles_ids:
        print("No vehicles to seed rides, skipping")
        return
    drivers_ids = db.drivers.distinct("_id")
    if not drivers_ids:
        print("No drivers to seed rides, skipping")
        return
    lines_ids = db.lines.distinct("_id")
    if not lines_ids:
        print("No lines to seed rides, skipping")
        return
    for i in range(count):
        vehicle_id = faker.random_element(vehicles_ids)
        driver_id = faker.random_element(drivers_ids)
        line_id = faker.random_element(lines_ids)
        start_time = faker.date_this_decade()
        weekday = faker.random_element(Weekday).value
        ride = Ride(
            vehicle_id=vehicle_id,
            driver_id=driver_id,
            line_id=line_id,
            start_time=start_time,
            weekday=weekday,
        )
        result = rides_collection.insert_one(ride.model_dump())
        if result.acknowledged:
            total_added += 1
        printProgressBar(i + 1, count, length=50, prefix="rides")


def seed_stops(db: MongoDB, count: int):
    stops_collection = db.stops
    total_added = 0
    for i in range(count):
        name = faker.street_name()
        address = faker.street_address()
        stop_type = faker.random_element(StopType).value
        shelter = faker.boolean(chance_of_getting_true=70)
        seating = faker.boolean(chance_of_getting_true=70)
        longitude = faker.longitude()
        latitude = faker.latitude()
        coords = Coords(longitude=longitude, latitude=latitude)
        stop = Stop(
            name=name,
            address=address,
            type=stop_type,
            coords=coords,
            shelter=shelter,
            seating=seating,
        )
        result = stops_collection.insert_one(stop.model_dump())
        if result.acknowledged:
            total_added += 1
        printProgressBar(i + 1, count, length=50, prefix="stops")


def seed_ticket_types(db: MongoDB, count: int):
    raise NotImplementedError


def seed_tickets(db: MongoDB, count: int):
    raise NotImplementedError


def seed_fines(db: MongoDB, count: int):
    raise NotImplementedError


def seed_inspections(db: MongoDB, count: int):
    inspections_collection = db.inspections
    inspectors = [
        InspectorInfo.from_inspector(Inspector(**inspector))
        for inspector in db.inspectors.find()
    ]
    if not inspectors:
        print("No inspectors to seed inspections, skipping")
        return
    rides_ids = db.rides.distinct("_id")
    if not rides_ids:
        print("No rides to seed inspections, skipping")
        return
    total_added = 0
    for i in range(count):
        inspector = faker.random_element(inspectors)
        ride_id = faker.random_element(rides_ids)
        date = faker.date_this_decade()
        inspection = Inspection(
            inspector=inspector, ride_id=ride_id, inspection_date=date
        )
        result = inspections_collection.insert_one(inspection.model_dump())
        if result.acknowledged:
            total_added += 1
        printProgressBar(i + 1, count, length=50, prefix="inspections")


def __generate_user_data() -> Tuple[str, str, str, str, Contact]:
    name: str = faker.first_name()
    surname: str = faker.last_name()
    login: str = faker.user_name()
    password: str = faker.password()
    email: str = faker.email()
    phone: str = "".join(
        str(faker.random_number(1)) for _ in range(faker.random_int(9, 15))
    )
    contact = Contact(email=email, phone=phone if faker.boolean() else None)
    return name, surname, login, password, contact


def __generate_path(stops: List[Stop]) -> List[PathItem]:
    path = []
    length = faker.random_int(min=2, max=len(stops) - 1)
    minute = 0
    randomized_stops = faker.random_sample(elements=stops, length=length)

    for i, stop in enumerate(randomized_stops):
        path_item = PathItem.from_stop(
            stop, i, minute + faker.random_int(min=2, max=10)
        )
        minute = path_item.minute
        path.append(path_item)
    return path


# Print iterations progress
def printProgressBar(
    iteration,
    total,
    prefix="elements",
    decimals=1,
    length=100,
    fill="█",
    printEnd="\r",
):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + "-" * (length - filledLength)
    print(
        f"\rAdding {total} {prefix} |{bar}| {percent}% {iteration}/{total}",
        end=printEnd,
    )
    # Print New Line on Complete
    if iteration == total:
        print()


if __name__ == "__main__":
    db = MongoDB()
    seed_inspections(db, 10)
