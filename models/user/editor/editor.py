from models.user.user import User


class Editor(User):
    pass


if __name__ == "__main__":
    from models.user.contact import Contact

    my_editor = Editor(
        name="John",
        surname="Doe",
        login="johndoe",
        password="password",
        contact=Contact(email="editor@editor.editor"),
    )

    print(my_editor.model_dump())
