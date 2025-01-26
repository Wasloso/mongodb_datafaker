from models.enums import Weekday
from models.model import Model
from bson import ObjectId
from datetime import datetime


class Ride(Model):
    line_id: ObjectId
    vehicle_id: ObjectId
    driver_id: ObjectId
    weekday: Weekday
    start_time: datetime
