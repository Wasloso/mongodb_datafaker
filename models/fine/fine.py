from __future__ import annotations  # Enable forward references
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING
from bson import ObjectId, Decimal128
from pydantic import BaseModel, Field
from models.default_config import DefaultConfig
from models.enums import FineStatus
from models.model import Model

from models.user.passenger.passenger_info import PassengerInfo


class Fine(Model):

    passenger_info: PassengerInfo
    status: FineStatus
    issued_by: ObjectId
    amount: Decimal = Field(ge=0.01, multiple_of=0.01)
    issue_date: datetime
    deadline: datetime
