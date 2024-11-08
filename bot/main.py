# Telegram Lunch Bot

Telegram bot for lunch matching among users based on their preferences and lunch time.
Telegram-бот для подбора компании на обед в зависимости от предпочтений и времени обеда.


## Функционал
- Мэтчинг пользователей для обеда.
- Настройка предпочтений пользователей.
- Уведомления о подходящих партнёрах по обеду.


## Требования
- Python 3.7+
- PostgreSQL
- Библиотеки: `python-telegram-bot`, `psycopg2`

## Установка
### 1. Клонируйте репозиторий

bash
git clone https://github.com/Anika1d/LunchBot.git
cd lunch-bot


### 2. Создайте и активируйте виртуальное окружение

bash
python -m venv venv
source venv/bin/activate  # Для Linux/Mac
venv\Scripts\activate  # Для Windows


### 3. Установите зависимости

bash
pip install -r requirements.txt


### 4. Настройте PostgreSQL
1. Установите PostgreSQL - https://www.postgresql.org/download/
3. Создайте новую базу данных для вашего бота.
4. Обновите строку подключения в коде, чтобы настроить доступ к вашей базе данных.


### 5. Запустите бота
Убедитесь, что вы правильно настроили токен вашего бота.  
Замените `YOUR_BOT_TOKEN` на токен, полученный от [BotFather](https://t.me/botfather).


Запустите скрипт:

bash
python main.py


## Использование
После запуска бота вы можете начать взаимодействовать с ним, отправив команду `/start`. затем настраивайте свои предпочтения и находите партнёров для обеда!


## Контакты
Dasevil
Jashu9an
Anika1d
Alex-ITop
NZRprog
