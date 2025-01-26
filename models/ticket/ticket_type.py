from decimal import Decimal

from pydantic import Field
from models.enums import TicketPeriodType
from models.model import Model
from models.ticket.price import Price


class TicketType(Model):
    name: str = Field(min_length=3, description="Must be at least 3 characters long.")
    price: Price
    duration: int = Field(gt=0, description="Must be greater than 0.")
    type: TicketPeriodType

    def model_dump(self):
        data = super().model_dump()
        if isinstance(self.price, Price):
            data["price"] = self.price.model_dump()
        return data


if __name__ == "__main__":
    my_ticket_type = TicketType(
        name="One way ticket",
        price=Price(normal=Decimal("10.00"), discounted=Decimal("5.00")),
        duration=60,
        type=TicketPeriodType.ALL,
    )
    print(my_ticket_type.model_dump())
