from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field


class Price(BaseModel):
    normal: Decimal = Field(ge=0.01, description="Must be greater than 0.")
    discounted: Optional[Decimal] = Field(
        ge=0.01, description="Must be greater than 0.", default=None
    )


if __name__ == "__main__":
    my_price = Price(normal=Decimal("10.00"), discounted=Decimal("5.00"))
    print(my_price.model_dump())
