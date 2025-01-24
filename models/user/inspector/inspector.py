from bson import ObjectId
from pydantic import BaseModel
from models.default_config import DefaultConfig
from models.user.user import User


class Inspector(User):
    pass


class InspectorInfo(BaseModel):
    model_config = DefaultConfig.config
    inspector_id: ObjectId
    name: str
    surname: str

    @classmethod
    def from_inspector(cls, inspector: "Inspector") -> "InspectorInfo":
        return cls(
            inspector_id=inspector.id, name=inspector.name, surname=inspector.surname
        )


if __name__ == "__main__":
    from models.user.contact import Contact

    my_inspector = Inspector(
        name="John",
        surname="Doe",
        login="johndoe",
        password="password",
        contact=Contact(email="inspector@inspector.inspector"),
    )
    print(my_inspector.model_dump())
