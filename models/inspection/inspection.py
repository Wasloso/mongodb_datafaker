from datetime import datetime
from models.model import Model
from bson import ObjectId

from models.user.inspector.inspector import InspectorInfo


class Inspection(Model):
    inspector: InspectorInfo
    ride_id: ObjectId
    date: datetime


if __name__ == "__main__":
    from models.user.inspector.inspector import *
    from models.user.contact import Contact

    inspector = Inspector(
        name="John",
        surname="Doe",
        login="login",
        password="password",
        contact=Contact(email="john@john.john"),
    )

    inspection = Inspection(
        inspector=InspectorInfo.from_inspector(inspector),
        date=datetime.now(),
        ride_id=ObjectId(),
    )

    print(inspection.model_dump())
