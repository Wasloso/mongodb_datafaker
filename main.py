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
        seed_vehicles: 100,
        seed_passengers: 5000,
        seed_drivers: 250,
        seed_editors: 10,
        seed_inspectors: 100,
        seed_stops: 250,
        seed_lines: 100,
        seed_rides: 10000,
        seed_ticket_types: 10,
        seed_tickets: 10000,
        seed_inspections: 2500,
        seed_fines: 3500,
    }
    for seed_function, count in seed_config.items():
        if count > 0:
            seed_function(db, count)


if __name__ == "__main__":
    main()
