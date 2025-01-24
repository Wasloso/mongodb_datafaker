from datetime import datetime
from decimal import Decimal
from bson import ObjectId
from pydantic import Field
from models.enums import FineStatus
from models.model import Model
from models.user.passenger.passenger import PassengerInfo


class Fine(Model):
    passenger_info: PassengerInfo
    status: FineStatus
    issued_by: ObjectId
    amount: Decimal = Field(ge=0.01, multiple_of=0.01)
    issue_date: datetime
    deadline: datetime


if __name__ == "__main__":
    fine = Fine(
        passenger_info=PassengerInfo(
            passenger_id=ObjectId(),
            email="passenger@passenger.com",
        ),
        status=FineStatus.UNPAID,
        issued_by=ObjectId(),
        amount=Decimal(10.25),
        deadline=datetime.now(),
        issue_date=datetime.now(),
    )

    print(fine.model_dump())
