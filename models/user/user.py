from pydantic import Field

from models.user.contact import Contact
from models.model import Model


class User(Model):
    name: str
    surname: str
    login: str = Field(min_length=3, description="Must be at least 6 characters long.")
    password: str = Field(
        min_length=6, description="Must be at least 6 characters long."
    )
    contact: Contact


if __name__ == "__main__":
    my_user = User(
        name="John",
        surname="Doe",
        login="johndoe",
        password="password",
        contact=Contact(email="contact@contact.contact"),
    )
    print(my_user.model_dump())
