from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field
from models.stop.stop import Stop


class PathItem(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    stop_id: ObjectId
    name: str
    order: int = Field(ge=0, multiple_of=1)
    minute: int = Field(ge=0, multiple_of=1)

    @classmethod
    def from_stop(cls, stop: Stop, order: int, minute: int) -> "PathItem":
        return cls(stop_id=stop.id, name=stop.name, order=order, minute=minute)


if __name__ == "__main__":
    from models.enums import StopType
    from models.stop.coords import Coords

    pathItem = PathItem(stop_id=ObjectId(), name="most grunwaldzki", order=1, minute=1)
    print(pathItem.model_dump())

    stop = Stop(
        name="most grunwaldzki",
        coords=Coords(latitude=20, longitude=10),
        type=StopType.BUS,
    )
    pathItemFromStop = PathItem.from_stop(stop, 10, 20)
    print(pathItemFromStop.model_dump())
