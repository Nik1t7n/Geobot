import random
import telebot
import json

photo_dict = {
    "https://imgur.com/a/RLzta7G": "Гранд Каньон Аризона США",
    "https://imgur.com/a/6kZ7Tsn": "Каньон Антилопы Аризона США",
    "https://imgur.com/a/T1Y46a6": "Каньон Подкова Аризона США",
    "https://imgur.com/a/UkvelEJ": "Долина Монументов Аризона Юта США",
    "https://imgur.com/a/qhBTKWw": "Брайс-Каньон Юта США",
    "https://imgur.com/a/o9N5Z8L": "Дыра Славы Озеро Берриесса США",
    "https://imgur.com/a/ujX1Sjm": "Ниагарский Водопад США Канада",
    "https://imgur.com/a/CgWWx5f": "Великий Призматический Источник Йеллоустонский Национальный Парк США",
    "https://imgur.com/a/Zs3PBxF": "Гейзер Флай Невада США",
    "https://imgur.com/a/NOzyXnr": "Мост Золотые Ворота Сан-Франциско США",
    "https://imgur.com/a/opZ1pHn": "Гора Рашмор Мемориал Президентам США",
    "https://imgur.com/a/lqGP4jy": "Монумент Вашингтона США",
    "https://imgur.com/a/X4yuuzJ": "Национальный Парк Секвойя США",
    "https://imgur.com/a/bLw5TfM": "Центральный Парк Нью-Йорк США",
    "https://imgur.com/a/6UdMMHb": "Пещеры Ледника Менденхолла Аляска США",
    "https://imgur.com/a/t83AlmH": "Национальный Парк Банф Канада",
    "https://imgur.com/a/YXXO4vv": "Монреальский Ботанический Сад Канада",
    "https://imgur.com/a/7R1RdM7": "Висячий Мост Капилано Ванкувер Канада",
    "https://imgur.com/a/bwFquZJ": "Си Эн Тауэр Торонто Канада",
    "https://imgur.com/a/axodcZk": "Пустыня Данакиль Эфиопия Африка",
    "https://imgur.com/a/u6PEBKN": "Аллея Баобабов Мадагаскар Африка",
    "https://imgur.com/a/afMWgVL": "Каменный Лес Мадагаскар Цинги-де-Бемараха",
    "https://imgur.com/a/AZejamB": "Луксор Египет Африка",
    "https://imgur.com/a/SCTJy6t": "Гора Килиманджаро Танзания Африка",
    "https://imgur.com/a/tUYfN7Q": "Гора Столовая ЮАР Африка",
    "https://imgur.com/a/iVYL0M8": "Колыбель Человечества ЮАР Африка",
    "https://imgur.com/a/CgEhQrx": "Томбукту Мали Африка",
    "https://imgur.com/a/Es5EB4Y": "Водопад Виктория Замбия Африка",
    "https://imgur.com/a/Upbjw0I": "Берег Скелетов Намибия"
}




# Загрузка данных из JSON-файла
def load_country_descriptions(file_path):
    with open(file_path, 'r', encoding='utf-8') as json_file:
        country_dict = json.load(json_file)

    return country_dict

# Загрузка данных из базы фотографий
def load_photo_dict(photo_dict):
    photo_data = {}
    for photo_url, answer in photo_dict.items():
        photo_data[photo_url] = answer

    return photo_data

# Выбор случайного описания для страны
def get_random_country_description(country_dict):
    country = random.choice(list(country_dict.keys()))
    descriptions = country_dict[country]
    description = random.choice(descriptions)
    return country, description

# Выбор случайной фотографии и ответа
def get_random_photo(photo_data):
    photo_url = random.choice(list(photo_data.keys()))
    answer = photo_data[photo_url]
    return photo_url, answer

def check_photo(answer, expected_answer):
    for url, description in photo_dict.items():
        if answer == description:
            return True
    return False

# Проверка ответа пользователя
def check_answer(user_answer, answer):
    return user_answer.lower() == answer.lower()

# Отправка нового описания страны пользователю
def send_new_country_description(message):
    country, description = get_random_country_description(country_descriptions)
    formatted_description = f"<i>{description}</i>"
    bot.send_message(message.chat.id, f"<b>Описание страны:</b>\n{formatted_description}", parse_mode='HTML')
    user_data[message.chat.id] = (country, description)

# Отправка новой фотографии пользователю
def send_new_photo(message):
    photo_url, answer = get_random_photo(photo_data)
    bot.send_photo(message.chat.id, photo_url)
    user_data[message.chat.id] = (photo_url, answer)

# Перезагрузка бота и восстановление описаний и фотографий
def reload_bot(message):
    global country_descriptions, photo_data
    country_descriptions = load_country_descriptions('descriptions.json')
    photo_data = load_photo_dict(photo_dict)
    send_new_country_description(message)

# Загрузка данных из JSON-файла
country_descriptions = load_country_descriptions('descriptions.json')

# Загрузка базы фотографий
photo_data = load_photo_dict(photo_dict)

# Настройка токена бота
bot = telebot.TeleBot('6116570275:AAEdNShJXJxaEVENGlollLzhMaNZf5fttfg')

# Словарь для хранения текущего состояния пользователя
user_data = {}

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Здравствуйте, введите команду /places, чтобы перейти к достопримечательностям, или /countries, чтобы отгадывать страны по описанию.", parse_mode='HTML')

# Обработчик команды /countries
@bot.message_handler(commands=['countries'])
def handle_countries(message):
    send_new_country_description(message)

# Обработчик команды /places
@bot.message_handler(commands=['places'])
def handle_places(message):
    send_new_photo(message)

# Обработчик ответов пользователя
# Обработчик ответов пользователя
# Обработчик ответов пользователя
@bot.message_handler(func=lambda message: True)
def handle_user_answer(message):
    chat_id = message.chat.id
    if chat_id in user_data:
        user_answer = message.text
        if isinstance(user_data[chat_id], tuple):
            country, description = user_data[chat_id]
            if check_answer(user_answer, country):
                bot.send_message(chat_id, "Правильный ответ! 🎉")
                del user_data[chat_id]
                descriptions = country_descriptions[country]
                descriptions.remove(description)
                if len(descriptions) == 0:
                    del country_descriptions[country]
                if not country_descriptions:
                    bot.send_message(chat_id, "Описания для всех стран закончились. Пожалуйста, используйте команду /countries, чтобы получить новые описания.")
                else:
                    send_new_country_description(message)
            elif check_photo(user_answer, photo_dict):
                bot.send_message(chat_id, "Правильный ответ на фотографию! 🎉")
                photo_url, answer = user_data[chat_id]
                del user_data[chat_id]
                del photo_data[photo_url]
                if not photo_data:
                    bot.send_message(chat_id, "Все фотографии просмотрены. Пожалуйста, используйте команду /places, чтобы получить новые фотографии.")
                else:
                    send_new_photo(message)
            else:
                bot.send_message(chat_id, "Неправильный ответ. Попробуйте ещё раз!")
        else:
            photo_url, answer = user_data[chat_id]
            if check_answer(user_answer, answer):
                bot.send_message(chat_id, "Правильный ответ! 🎉")
                del user_data[chat_id]
                del photo_data[photo_url]
                if not photo_data:
                    bot.send_message(chat_id, "Все фотографии просмотрены. Пожалуйста, используйте команду /places, чтобы получить новые фотографии.")
                else:
                    send_new_photo(message)
            else:
                bot.send_message(chat_id, "Неправильный ответ. Попробуйте ещё раз!")


# Обработчик команды /reload
@bot.message_handler(commands=['reload'])
def handle_reload(message):
    reload_bot(message)

# Запуск бота
bot.polling()
