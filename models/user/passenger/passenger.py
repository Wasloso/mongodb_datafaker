from typing import List, Optional
from bson import ObjectId
from pydantic import BaseModel, Field
from models.default_config import DefaultConfig
from models.fine.fine import UnpaidFine
from models.ticket.ticket import ActiveTicket
from models.user.user import User


class Passenger(User):
    active_tickets: List[ActiveTicket] = Field(required=False, default=[])
    unpaid_fines: List[UnpaidFine] = Field(required=False, default=[])


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


if __name__ == "__main__":
    from models.user.contact import Contact

    passenger = Passenger(
        name="Johm",
        surname="Doe",
        login="Johnjohn",
        password="johnjohn",
        contact=Contact(email="john@john.john"),
    )

    passenger_info = PassengerInfo.from_passenger(passenger)
    print(passenger_info.model_dump())
