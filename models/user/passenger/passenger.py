from typing import List
from pydantic import Field
from models.fine.unpaid_fine import UnpaidFine
from models.ticket.ticket import ActiveTicket
from models.user.user import User


class Passenger(User):
    active_tickets: List[ActiveTicket] = Field(required=False, default=[])
    unpaid_fines: List[UnpaidFine] = Field(required=False, default=[])
