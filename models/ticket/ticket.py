from datetime import datetime
from bson import ObjectId
from pydantic import BaseModel, Field
from models.default_config import DefaultConfig
from models.enums import TicketStatus
from models.model import Model
from models.ticket.purchase import Purchase
from models.ticket.validity_info import ValidityInfo
from models.ticket.ticket_type import TicketType


class Ticket(Model):
    ticket_type_id: ObjectId
    user_id: ObjectId
    purchase: Purchase
    status: TicketStatus
    validity_info: ValidityInfo

    def model_dump(self):
        data = super().model_dump()
        if isinstance(self.purchase, Purchase):
            data["purchase"] = self.purchase.model_dump()
        return data


class ActiveTicket(BaseModel):
    model_config = DefaultConfig.config
    ticket_id: ObjectId
    name: str = Field(required=False)
    valid_until: datetime = Field(required=False)

    @classmethod
    def from_ticket(cls, ticket: "Ticket", ticketType: TicketType) -> "ActiveTicket":
        return cls(
            ticket_id=ticket.id,
            name=ticketType.name,
            valid_until=ticket.validity_info.valid_untill,
        )
