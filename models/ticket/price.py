from decimal import Decimal
from typing import Optional
from bson import Decimal128
from pydantic import BaseModel, Field, field_validator


class Price(BaseModel):
    normal: Decimal = Field(ge=0.01, description="Must be greater than 0.")
    discounted: Optional[Decimal] = Field(
        ge=0.01, description="Must be greater than 0.", default=None
    )

    @field_validator("normal", "discounted", mode="before")
    def convert_decimal128_to_decimal(cls, value):
        if isinstance(value, Decimal128):
            return value.to_decimal()
        return value

    def model_dump(self):
        data = {
            "normal": Decimal128(str(self.normal)),
        }
        if self.discounted:
            data["discounted"] = Decimal128(str(self.discounted))
        return data


if __name__ == "__main__":
    my_price = Price(normal=Decimal("10.00"), discounted=Decimal("5.00"))
    print(my_price.model_dump())
