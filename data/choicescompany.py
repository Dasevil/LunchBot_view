from enum import Enum


from data.user import  UserSex


class ChoicesCompany(Enum):
    MALE = UserSex.MALE.value
    FEMALE = UserSex.FEMALE.value
    COMPANY = "company"

    def toRus(self):
        match (self):
            case ChoicesCompany.MALE.value:
                return UserSex.MALE.toRus()
            case ChoicesCompany.FEMALE.value:
                return UserSex.FEMALE.toRus()
            case ChoicesCompany.COMPANY:
                return "Компания"
