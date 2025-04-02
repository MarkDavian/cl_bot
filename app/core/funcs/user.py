from app.core.db.database import Users
from app.core.types.types import UserBuilder, User


def add_user(
        id,
        chat_notify,
        registration
) -> None:
    with Users() as storage:
        storage.add(
            UserBuilder(
                id,
                chat_notify,
                registration
            ).__dict__()
        )


def get_user(message) -> User:
    user_id = message.from_user.id

    with Users() as s:
        info = s.get_by_id(user_id)

    return UserBuilder(**info).get_user()


def get_all_to_notify() -> list[str]:
    to_notify = []
    with Users() as s:
        users = s.get()
        for с, item in enumerate(users):
            if item['chat_notify'] == True:
                to_notify.append(item['id'])
                
    return to_notify


def save_user(user: User) -> None:
    id = user.id
    with Users() as s:
        s.delete(id)

    add_user(**user.__dict__())