from telegram import ReplyKeyboardRemove, Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext, MessageHandler, ConversationHandler, filters
from telegram import ReplyKeyboardMarkup
from user import UserSex, User
import logging
from uuid import uuid4

# Логгинг
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# КХ
REGISTER, GET_NAME, GET_SEX, GET_PARTNER_PREFERENCE, GET_LUNCH_TIME, PREFERENCES, FEEDBACK = range(7)

# Пародия на БД
users = {}
lunch_matches = {}
feedbacks = {}

# Функция для создания навигационного меню
async def show_navigation_menu(update: Update, context: CallbackContext) -> None:
    """Отображает меню навигации в виде кнопок."""
    navigation_buttons = ReplyKeyboardMarkup(
        [
            ["/start", "/find_buddy"],
            ["/feedback"],
        ],
        resize_keyboard = True,  # Чтобы кнопки подстраивались под экран
        one_time_keyboard = False,  # Чтобы кнопки оставались постоянно
    )
    await update.message.reply_text( "Выберите команду из списка ниже:",
        reply_markup = navigation_buttons
    )


# Добавляем отображение меню навигации в командах
async def start(update: Update, context: CallbackContext) -> int:
    """Стартовая команда с отображением меню навигации."""
    await update.message.reply_text(
        "Привет! 👋 \n"
        "Ты попал в LunchBuddy – бота, который поможет тебе найти классную компанию для обеда!\n"
        "Чтобы найти идеальных сотрапезников, ответь на пару вопросов о себе и заполни короткую анкету.\n"
        "Поехали! 🚀\n\n"
        "Введите имя (или псевдоним):"
    )
    return GET_NAME 

# Имя
async def get_name(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id
    name = update.message.text
    if name.startswith('/'):
        await update.message.reply_text(
            "Неверный формат имени. Пожалуйста, введите иначе."
        )
        return GET_NAME
    users[user_id] = {"username": update.message.from_user.username, "name": name}

    await update.message.reply_text("Пол:", reply_markup=ReplyKeyboardMarkup([["Мужской", "Женский"]], one_time_keyboard=True))
    return GET_SEX

# Пол
async def get_sex(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id
    sex = UserSex.MALE if update.message.text == "Мужской" else UserSex.FEMALE
    users[user_id]["sex"] = sex
    # await update.message.reply_text(
    #     "Выберите, с кем Вам было бы комфортно обедать?", 
    #     reply_markup=ReplyKeyboardMarkup([["Девушка", "Парень", "Компания", "Неважно"]], one_time_keyboard=True)
    # )

    await update.message.reply_text(
        "Выберите, с кем Вам было бы комфортно обедать?", 
        reply_markup=ReplyKeyboardMarkup([["Девушка", "Парень", "Неважно"]], one_time_keyboard=True)
    )
    return GET_PARTNER_PREFERENCE

# async def find_buddies(update: Update, context: CallbackContext) -> None:
#     user_id = update.message.from_user.id
#     user_pref = users.get(user_id, {}).get("partner_preference")
#     user_lunch_time = users.get(user_id, {}).get("lunch_time")

#     if user_pref is None or user_lunch_time is None:
#         await context.bot.send_message(chat_id=user_id, text="Укажите ваши предпочтения и время обеда!")
#         return

#     matching_groups = []
#     for uid, data in users.items():
#         if uid != user_id:
#             pref = data.get("partner_preference")
#             lunch_time = data.get("lunch_time")
#             username = data.get("username") # Добавлена проверка на наличие username

#             #Проверка на наличие всех необходимых данных
#             if pref is not None and lunch_time is not None and username is not None:
#                 if (user_pref, user_lunch_time) == (pref, lunch_time):
#                     matching_groups.append(uid)


#     if len(matching_groups) == 4: #нужно минимум 2 человека, так как мы добавляем  пользователя в список
#         suitable_buddies = matching_groups + [user_id]
#         usernames = [f"@{users[uid]['username']}" for uid in suitable_buddies]
#         message = f"Для обеда подходят: {', '.join(usernames)}"
#         await context.bot.send_message(chat_id=user_id, text=message)
#     else:
#         await context.bot.send_message(chat_id=user_id, text="Пока нет подходящих людей для обеда.")


# Префы
async def get_partner_preference(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id
    users[user_id]["partner_preference"] = update.message.text
    await update.message.reply_text(
        "Желаемое время обеда:", 
        reply_markup=ReplyKeyboardMarkup(
            [["12:00-13:00", "13:00-14:00", "14:00-15:00"], ["15:00-16:00", "16:00-17:00"]],
            one_time_keyboard=True
        )
    )
    return GET_LUNCH_TIME

# Время
async def get_lunch_time(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id
    users[user_id]["lunch_time"] = update.message.text
    
    await update.message.reply_text(
        f"Вы успешно зарегистрированы. Приятного аппетита! ", reply_markup = ReplyKeyboardRemove()
    )
    
    await update.message.reply_text(
        "🍕 Нажмите кнопку ниже, чтобы найти компаньона на обед! 🍕", reply_markup = ReplyKeyboardMarkup(
            [["/find_buddy"]], 
            one_time_keyboard = True, 
            resize_keyboard = True
        )
    )

    return ConversationHandler.END

# Функция для регистрации предпочтений (опционально, пока пох я думаю)
async def save_preferences(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id
    users[user_id]["preferences"] = update.message.text
    await update.message.reply_text("Ваши предпочтения сохранены.")
    return ConversationHandler.END

# Мэтчинг
async def find_buddy(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    user_pref = users[user_id].get("partner_preference")
    user_lunch_time = users[user_id].get("lunch_time")
    
    for uid, data in users.items():
        # Мэтч
        if uid != user_id and data.get("partner_preference") == user_pref and data.get("lunch_time") == user_lunch_time:
            lunch_matches[user_id] = uid
            lunch_matches[uid] = user_id
            await context.bot.send_message(chat_id=user_id, text=f"Для обеда подходит: @{users[uid]['username']}")
            await context.bot.send_message(chat_id=uid, text=f"Для обеда подходит: @{users[user_id]['username']}")
            return
    
    await update.message.reply_text("Пока не удалось найти подходящего напарника для обеда. Попробуйте, пожалуйста, позже.")

# Ремайндер
async def remind(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    match_id = lunch_matches.get(user_id)
    
    if match_id:
        await context.bot.send_message(
            chat_id=user_id, 
            text=f"Напоминаем: у Вас запланирован обед с @{users[match_id]['username']}!"
        )
    else:
        await update.message.reply_text("У Вас нет запланированных встреч на обед.")

# Сохранение фидбека
async def save_feedback(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id
    score, *review = update.message.text.split(maxsplit=1)
    score = float(score)
    review = review[0] if review else ""
    
    if user_id in lunch_matches:
        partner_id = lunch_matches[user_id]
        
        # Обновление рейтинга (возможно это нахрен не надо, обсудите и удалите если что)
        if "rating" in users[partner_id]:
            users[partner_id]["rating"] = (users[partner_id]["rating"] + score) / 2
        else:
            users[partner_id]["rating"] = score
        
        # Сохранение отзыва
        feedbacks[user_id] = {"partner_id": partner_id, "score": score, "review": review}
        await update.message.reply_text("Спасибо за отзыв! Ваш отзыв был сохранён.")
    else:
        await update.message.reply_text("Обед не состоялся, оставить отзыв нельзя.")
    
    return ConversationHandler.END

async def feedback(update: Update, context: CallbackContext) -> int:
    await show_navigation_menu(update, context)
    await update.message.reply_text(
        "Оцените Ваш обед:", 
        reply_markup=ReplyKeyboardMarkup(
            [["1", "2", "3"], ["4", "5"]],
            one_time_keyboard=True,
            resize_keyboard=True
        )
    )
    return FEEDBACK

async def feedback_received(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text(
        "Спасибо за Ваш отзыв! \n"
        "Редактируйте Вашу анкету или начните поиск заново!",
        reply_markup=ReplyKeyboardMarkup(
            [["/start", "/find_buddy"]], 
            resize_keyboard=True,
            one_time_keyboard=True
        )
    )
    return ConversationHandler.END

# async def edit_profile(update: Update, context: CallbackContext) -> int:
#     """Команда для редактирования анкеты с меню навигации."""
#     user_id = update.message.from_user.id
#     if user_id in users:
#         del users[user_id]  # Удаляем данные пользователя (опционально)

#     context.user_data.clear()

#     await show_navigation_menu(update, context)
#     await update.message.reply_text(
#         "Вы начали редактирование профиля. Анкета будет заполнена заново. Введите имя:", reply_markup = ReplyKeyboardRemove()
#     )
#     return GET_NAME

async def help_command(update: Update, context: CallbackContext) -> None:

    await update.message.reply_text(
        "🤖 Доступные команды:\n\n"
        "/start - Начать регистрацию и заполнение анкеты\n"
        "/find_buddy - Найти напарника для обеда\n"
        "/feedback - Оставить отзыв о проведенном обеде\n"
        # "/edit_profile - Редактировать свою анкету (перезапуск регистрации)\n\n"
    )
    await show_navigation_menu(update, context)

def main() -> None:
    application = Application.builder().token("7700731666:AAESsLAY8Bu_KNNYBm3KCAL4ugKZWGVzbGw").build()

    # рег
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            GET_NAME: [MessageHandler(filters.TEXT, get_name)],
            GET_SEX: [MessageHandler(filters.TEXT, get_sex)],
            GET_PARTNER_PREFERENCE: [MessageHandler(filters.TEXT, get_partner_preference)],
            GET_LUNCH_TIME: [MessageHandler(filters.TEXT, get_lunch_time)],
            PREFERENCES: [MessageHandler(filters.TEXT, save_preferences)],
            FEEDBACK: [MessageHandler(filters.TEXT, save_feedback)],
        },
        fallbacks=[]
    )
    application.add_handler(conv_handler)

    # Другие команды
    application.add_handler(CommandHandler("find_buddy", find_buddy))
    application.add_handler(CommandHandler("remind", remind))
    application.add_handler(CommandHandler("feedback", feedback))
    application.add_handler(CommandHandler("help", help_command))
    # application.add_handler(CommandHandler("edit_profile", edit_profile))

    # Ланч
    application.run_polling()


if __name__ == "__main__":
    main()
