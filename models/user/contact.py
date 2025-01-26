from typing import Optional
from pydantic import BaseModel, Field


class Contact(BaseModel):
    email: str = Field(pattern="^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$")
    phone: Optional[str] = Field(pattern="[0-9]{9,15}", required=False, default=None)


if __name__ == "__main__":
    my_contact1 = Contact(email="email@email.com", phone="123456789")
    my_contact2 = Contact(email="email@email.com")
    print(my_contact1.model_dump())
    print(my_contact2.model_dump())
