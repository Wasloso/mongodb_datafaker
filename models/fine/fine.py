from __future__ import annotations  # Enable forward references
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING
from bson import ObjectId
from pydantic import BaseModel, Field
from models.default_config import DefaultConfig
from models.enums import FineStatus
from models.model import Model

if TYPE_CHECKING:
    from models.user.passenger.passenger import PassengerInfo


class Fine(Model):
    passenger_info: PassengerInfo
    status: FineStatus
    issued_by: ObjectId
    amount: Decimal = Field(ge=0.01, multiple_of=0.01)
    issue_date: datetime
    deadline: datetime


class UnpaidFine(BaseModel):
    model_config = DefaultConfig.config
    fine_id: ObjectId
    amount: Decimal = Field(ge=0.01, multiple_of=0.01, required=False)
    deadline: datetime = Field(required=False)

    @classmethod
    def from_fine(cls, fine: Fine) -> "UnpaidFine":
        return cls(
            fine_id=fine.id,
            amount=fine.amount,
            deadline=fine.deadline,
        )


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

    unpaid_fine = UnpaidFine.from_fine(fine)

    print(fine.model_dump())
    print(unpaid_fine.model_dump())
