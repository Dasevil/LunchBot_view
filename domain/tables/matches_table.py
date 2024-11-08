from domain.db import DATABASES


class MatchesTable:

    def __init__(self):
        self.db = DATABASES

    def create(self, userId: int, timeStart: float, timeFinish: float):
        self.db.startSearch(userId, timeStart, timeFinish)

    def cancel(self, userId: int):
        self.db.cancel(userId)

MATCHES_TABLE=MatchesTable()
