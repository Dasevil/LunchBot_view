from telegram import Bot

from data.choicescompany import ChoicesCompany
from data.preference import Preference
from data.user import User
from typing import Optional

from domain.tables.matches_table import MATCHES_TABLE


class ServicesMatches:
    waiting_users: list[tuple[User, Preference]] = []
    waiting_users_of_companies: list[tuple[User, Preference]] = []
    bot: Optional[Bot]
    matchesTable = MATCHES_TABLE

    def __init__(self, b: Optional[Bot]):
        self.bot = b

    async def add_user(self, user: User, preference: Preference):
        """Добавление пользователя в очередь и поиск пары."""
        matched_users = await self.find_match(user, preference)
        if len(matched_users) != 0:
            # Если нашлась пара, уведомляем обоих пользователей
            matched_users.append((user, preference))
            await self.notify_match(matched_users)
        else:
            # Если пары нет, добавляем пользователя в очередь ожидания
            if preference.company != ChoicesCompany.COMPANY:
                self.waiting_users.append((user, preference))
            else:
                self.waiting_users_of_companies.append((user, preference))
            await self.bot.send_message(user.chat_id, "Вы добавлены в очередь ожидания.")

    async def find_match(self, user: User, preference: Preference) -> list[tuple[User, Preference]]:
        """Проверяет, есть ли пользователь с похожими параметрами для встречи"""
        tmp_values = []
        tmp_index = []
        if preference.company != ChoicesCompany.COMPANY:
            for i in range(0, len(self.waiting_users)):
                other_user, other_preference = self.waiting_users[i]
                if ((other_user.telegram_id != user.telegram_id) &
                        (preference.company == other_preference.company) &
                        (preference.time_start == other_preference.time_start)
                ):
                    el = (other_user, other_preference)
                    tmp_values.append(el)
                    tmp_index.append(i)
                    break
        else:
            for i in range(0, len(self.waiting_users_of_companies)):
                other_user, other_preference = self.waiting_users_of_companies[i]
                if ((other_user.telegram_id != user.telegram_id) &
                        (preference.company == other_preference.company) &
                        (preference.time_start == other_preference.time_start)
                ):
                    el = (other_user, other_preference)
                    tmp_values.append(el)
                    tmp_index.append(i)
                    if 3 <= len(tmp_index):
                        break

        if preference.company != ChoicesCompany.COMPANY:
            for i in tmp_index:
                self.waiting_users.pop(i)
        else:
            for i in tmp_index:
                self.waiting_users_of_companies.pop(i)
        return tmp_values

    async def notify_match(self, users: list[tuple[User, Preference]]):
        """Отправляет сообщение пользователям о найденной паре."""
        for user, pref in users:
            MATCHES_TABLE.create(userId=user.telegram_id, timeStart=pref.time_start, timeFinish=pref.time_end)
            await self.bot.send_message(user.chat_id, "Мы нашли вам пару для встречи!")
