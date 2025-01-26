from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING
from bson import Decimal128, ObjectId
from pydantic import BaseModel, Field
from models.default_config import DefaultConfig

if TYPE_CHECKING:
    from models.fine.fine import Fine


class UnpaidFine(BaseModel):
    model_config = DefaultConfig.config
    fine_id: ObjectId
    amount: Decimal128
    deadline: datetime = Field(required=False)

    @classmethod
    def from_fine(cls, fine: "Fine") -> "UnpaidFine":
        amount = Decimal128(str(fine.amount))
        return cls(
            fine_id=fine.id,
            amount=amount,
            deadline=fine.deadline,
        )
