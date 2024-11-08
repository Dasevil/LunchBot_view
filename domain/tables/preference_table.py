from domain.db import DATABASES


class PreferenceTable:
    def __init__(self):
        self.db = DATABASES

    def create_preference(self, user_id: int):
        self.db.create_preference(user_id)
