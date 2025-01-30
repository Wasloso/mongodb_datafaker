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
    seed_tech_issues,
    seed_ticket_types_predefined,
)


def main():
    db: MongoDB = MongoDB()
    seed_config = {
        seed_vehicles: 750,
        seed_passengers: 10000,
        seed_drivers: 2500,
        seed_editors: 10,
        seed_inspectors: 250,
        seed_stops: 500,
        seed_lines: 250,
        seed_rides: 5000,
        seed_ticket_types_predefined: 1,
        seed_tickets: 5000,
        seed_inspections: 2500,
        seed_fines: 5000,
        seed_tech_issues: 1000,
    }
    db.clear_database()

    for seed_function, count in seed_config.items():
        if count > 0:
            seed_function(db, count)


if __name__ == "__main__":
    main()
