from enum import Enum


class VehicleStatus(str, Enum):
    ACTIVE: str = "active"
    INACTIVE: str = "inactive"
    UNDER_MAINTENANCE: str = "under maintenance"


class VehicleType(str, Enum):
    BUS: str = "bus"
    TRAM: str = "tram"


class TechnicalIssueStatus(str, Enum):
    REPORTED: str = "reported"
    RESOLVED: str = "resolved"


class StopType(str, Enum):
    BUS: str = "bus"
    TRAM: str = "tram"
    MIXED: str = "mixed"


class TicketStatus(str, Enum):
    ACTIVE: str = "active"
    USED: str = "used"
    EXPIRED: str = "expired"
    RETURNED: str = "returned"


class TicketPeriodType(str, Enum):
    SINGLE: str = "one-way"
    ALL: str = "all"
    TWOLINES: str = "two-lines"
    PATH: str = "path"


class FineStatus(str, Enum):
    PAID = "paid"
    UNPAID = "unpaid"


class Weekday(str, Enum):
    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"
