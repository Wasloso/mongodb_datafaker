from bson import ObjectId
from models.enums import TicketStatus
from models.model import Model
from models.ticket.purchase import Purchase


class Ticket(Model):
    ticket_type_id: ObjectId
    user_id: ObjectId
    purchase: Purchase
    status: TicketStatus
    validity_info: ValidityInfo
