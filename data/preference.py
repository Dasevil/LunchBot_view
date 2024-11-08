from data.choicescompany import ChoicesCompany


class Preference:
    def __init__(self, id: int, user_id: int, time_start: float, time_end: float, company: ChoicesCompany,):
        self.id = id
        self.user_id = user_id
        self.time_start = time_start
        self.time_end = time_end
        self.company = company
