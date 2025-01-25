from enum import Enum


class Collections(str, Enum):
    DRIVERS = "drivers"
    EDITORS = "editors"
    PASSENGERS = "passengers"
    INSPECTORS = "inspectors"
    INSPECTIONS = "inspections"
    FINES = "fines"
    VEHICLES = "vehicles"
    LINES = "lines"
    RIDES = "rides"
    STOPS = "stops"
    TICKET_TYPES = "ticket_types"
    TICKETS = "tickets"
