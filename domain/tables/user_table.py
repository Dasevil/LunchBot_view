from data.user import UserSex, UserStatus
from domain.db import DATABASES


class UserTable:

    def __init__(self):
        self.db = DATABASES

    def create_user(self, chatId: int, user_id: int):
        self.db.create_user(chat_id=chatId, user_id=user_id)

    def setUserName(self, name: str | None, user_id: int):
        self.db.set_user_name(name=name if (name is not None) else f"{user_id}", user_id=user_id)

    def setUserGender(self, sex: UserSex, user_id: int):
        self.db.set_user_gender(sex, user_id)

    def changeUserStatus(self, userStatus: UserStatus, user_id: int):
        self.db.setUserStatus(userStatus, user_id)


USER_TABLE = UserTable()
