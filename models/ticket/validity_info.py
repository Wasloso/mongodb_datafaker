from datetime import datetime
from typing import List, Optional
from bson import ObjectId
from pydantic import BaseModel, Field

from models.default_config import DefaultConfig
from models.enums import TicketPeriodType
from models.line.line import Line


class ValidityInfo(BaseModel):
    model_config = DefaultConfig.config
    valid_untill: datetime
    lines: Optional[List[Line]] = Field(default=None)
    ride_id: Optional[ObjectId] = Field(default=None)
    stops: Optional[List[ObjectId]] = Field(default=None)
    type: TicketPeriodType
