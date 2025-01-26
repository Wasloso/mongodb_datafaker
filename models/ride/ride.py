from models.model import Model
from models.vehicle.vehicle import Vehicle
from models.user.driver.driver import Driver
from models.line.line import Line
from models.default_config import DefaultConfig
from decimal import Decimal
from bson import Decimal128, ObjectId
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Ride(BaseModel):
    model_config = DefaultConfig.config
    id: ObjectId = Field(alias="_id", required=False, default=None)
    line_id: Line  = Field(required=True)
    vehicle_id: Vehicle = Field(required=True)
    driver_id: Driver = Field(required=True)
    weekday: str = Field(required=True)
    start_time: datetime= Field(required=True)

    def model_dump(
        self,
        *,
        mode="python",
        include=None,
        exclude=None,
        context=None,
        by_alias=True,
        exclude_unset=False,
        exclude_defaults=False,
        exclude_none=True,
        round_trip=False,
        warnings=True,
        serialize_as_any=False
    ):
        data = super().model_dump(
            mode=mode,
            include=include,
            exclude=exclude,
            context=context,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            round_trip=round_trip,
            warnings=warnings,
            serialize_as_any=serialize_as_any,
        )
        for key, value in data.items():
            if isinstance(value, Decimal):
                data[key] = Decimal128(value)
        return data




