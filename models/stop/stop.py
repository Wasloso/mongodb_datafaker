from ..model import Model
from ..enums import StopType
from .coords import Coords


class Stop(Model):
    name: str
    type: StopType
    seating: bool = (False,)
    shelter: bool = (False,)
    coords: Coords


if __name__ == "__main__":
    my_stop = Stop(
        seating=True,
        shelter=True,
        name="My Stop",
        type=StopType.MIXED,
        coords=Coords(longitude=19.456, latitude=51.759),
    )
    print(my_stop.model_dump())
