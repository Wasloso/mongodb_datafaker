from datetime import datetime

from pydantic import BaseModel


class License(BaseModel):
    id_license: str
    issued_on: datetime
    expires_on: datetime


if __name__ == "__main__":
    my_license = License(
        id_license="123456",
        issued_on=datetime.now(),
        expires_on=datetime.now(),
    )
    print(my_license.model_dump())
