from datetime import datetime
from decimal import Decimal

from bson import Decimal128
from pydantic import Field, field_validator
from ..enums import TechnicalIssueStatus
from ..model import Model


class TechnicalIssue(Model):
    description: str
    report_date: datetime
    resolve_date: datetime | None
    status: TechnicalIssueStatus
    repair_cost: Decimal | None = Field(gt=0, description="Must be greater than 0.")

    @field_validator("repair_cost", mode="before")
    def convert_decimal128_to_decimal(cls, value):
        if isinstance(value, Decimal128):
            return value.to_decimal()
        return value

    def model_dump(self):
        data = super().model_dump()
        if self.repair_cost:
            data["repair_cost"] = Decimal128(str(self.repair_cost))
        return data
