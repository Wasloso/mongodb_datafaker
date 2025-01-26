from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, Field
from models.default_config import DefaultConfig
from models.user.passenger.passenger import Passenger


class PassengerInfo(BaseModel):
    model_config = DefaultConfig.config
    passenger_id: ObjectId
    phone: Optional[str] = Field(default=None)
    email: Optional[str] = Field(default=None)

    @classmethod
    def from_passenger(cls, passenger: "Passenger") -> "PassengerInfo":
        return cls(
            passenger_id=passenger.id,
            phone=passenger.contact.phone,
            email=passenger.contact.email,
        )
