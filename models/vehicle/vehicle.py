from datetime import datetime
from decimal import Decimal
from typing import Literal, Optional, List
from pydantic import Field, field_validator
from ..enums import TechnicalIssueStatus, VehicleStatus, VehicleType
from ..model import Model
from models.vehicle.technical_issue import TechnicalIssue


class Vehicle(Model):
    number: str
    capacity: int = Field(ge=1, description="Must be greater than 0.")
    production_date: datetime
    type: VehicleType
    status: VehicleStatus
    air_conditioning: bool
    technial_issues: Optional[List[TechnicalIssue]] = Field(default=None)

    @field_validator("technial_issues", mode="before")
    def convert_technical_issues(cls, value):
        if value is None:
            return []
        return value

    def model_dump(self):
        data = super().model_dump()
        if self.technial_issues:
            data["technial_issues"] = [
                issue.model_dump() for issue in self.technial_issues
            ]
        return data


if __name__ == "__main__":
    my_vehicle = Vehicle(
        number="123",
        capacity=100,
        production_date=datetime(2020, 1, 1),
        type=VehicleType.BUS,
        status=VehicleStatus.ACTIVE,
        air_conditioning=True,
        technial_issues=[
            TechnicalIssue(
                description="Broken engine",
                report_date=datetime(2021, 1, 1),
                resolve_date=None,
                status=TechnicalIssueStatus.REPORTED,
                repair_cost=Decimal("1000.00"),
            ),
            TechnicalIssue(
                description="Broken door",
                report_date=datetime(2021, 2, 1),
                resolve_date=datetime(2021, 1, 1),
                status=TechnicalIssueStatus.RESOLVED,
                repair_cost=Decimal("500.00"),
            ),
        ],
    )
    print(my_vehicle.model_dump(by_alias=True, exclude_none=True))
