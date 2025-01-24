from models.user.driver.license import License
from models.user.user import User


class Driver(User):
    license: License


if __name__ == "__main__":
    from models.user.contact import Contact
    from datetime import datetime

    my_driver = Driver(
        name="John",
        surname="Doe",
        login="johndoe",
        password="password",
        contact=Contact(email="driver@driver.driver"),
        license=License(
            id_license="123456",
            issued_on=datetime.now(),
            expires_on=datetime.now(),
        ),
    )
    print(my_driver.model_dump())
