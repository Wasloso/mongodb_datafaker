from datetime import datetime
from decimal import Decimal

from pydantic import Field, field_validator
from ..enums import TechnicalIssueStatus
from ..model import Model


class TechnicalIssue(Model):
    description: str
    report_date: datetime
    resolve_date: datetime | None
    status: TechnicalIssueStatus
    repair_cost: Decimal | None = Field(gt=0, description="Must be greater than 0.")
