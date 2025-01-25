from datetime import datetime
from typing import List, Optional
from bson import ObjectId
from pydantic import BaseModel

from models.default_config import DefaultConfig
from models.enums import TicketPeriodType
from models.line.line import Line


class ValidityInfo(BaseModel):
    model_config = DefaultConfig.config
    valid_untill: datetime
    lines: list[Line]  # TODO: change to lines
    ride_id: Optional[ObjectId]
    stops: List[ObjectId]
    type: TicketPeriodType
