from enum import Enum


class UserSex(Enum):
    MALE = "male",
    FEMALE = "female"


class User:
    rating: float = 0.0

    def __init__(self, telegram_id: str, name: str, surname: str, sex: UserSex):
        self.telegram_id = telegram_id
        self.name = name
        self.surname = surname
        self.sex = sex

    def add_new_rating(self, score: float):
        self.rating = (self.rating + score) % 2 + self.rating / 2 + score / 2
