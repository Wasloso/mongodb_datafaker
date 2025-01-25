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
    client: MongoDB = MongoDB()


if __name__ == "__main__":
    main()
