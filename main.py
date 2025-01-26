from pymongo.collection import Collection
from database.connection import MongoDB
from seeder.seed import (
    seed_passengers,
    seed_drivers,
    seed_editors,
    seed_inspectors,
    seed_vehicles,
    seed_lines,
    seed_rides,
    seed_stops,
    seed_ticket_types,
    seed_tickets,
    seed_fines,
    seed_inspections,
)


def main():
    db: MongoDB = MongoDB()
    seed_config = {
        seed_vehicles: 10,
        seed_passengers: 10,
        seed_drivers: 10,
        seed_editors: 10,
        seed_inspectors: 10,
        seed_stops: 10,
        seed_lines: 10,
        seed_rides: 10,
        seed_ticket_types: 10,
        seed_tickets: 10,
        seed_inspections: 10,
        seed_fines: 10,
    }
    for seed_function, count in seed_config.items():
        if count > 0:
            seed_function(db, count)


if __name__ == "__main__":
    main()
