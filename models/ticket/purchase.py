from datetime import datetime
from decimal import Decimal
from bson import Decimal128
from pydantic import field_validator
from models.model import Model


class Purchase(Model):
    amount_paid: Decimal
    date: datetime

    @field_validator("amount_paid", mode="before")
    def convert_decimal128_to_decimal(cls, value):
        if isinstance(value, Decimal128):
            return value.to_decimal()  # Convert Decimal128 to Decimal
        return value

    def model_dump(self):
        return {
            "amount_paid": Decimal128(str(self.amount_paid)),
            "date": self.date,
        }
