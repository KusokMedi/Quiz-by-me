import telebot
from random import choice, shuffle

# Замените на ваш токен бота
bot = telebot.TeleBot('Your_token')

# Словарь с вопросами и ответами
questions = {
    "Что из перечисленного является возобновляемым ресурсом?": ["Солнечная энергия", "Уголь", "Нефть", "Природный газ"],
    "Какой вид энергии выделяется при сгорании угля?": ["Тепловая энергия", "Световая энергия", "Механическая энергия", "Звуковая энергия"],
    "Какой из этих отходов разлагается быстрее всего?": ["Бумага", "Пластик", "Металл", "Стекло"],
    "Какая из следующих мер уменьшает загрязнение воздуха?": ["Использование общественного транспорта", "Вырубка лесов", "Сжигание мусора", "Частое использование автомобиля"],
    "Какие лампы потребляют меньше всего энергии?": ["Светодиодные лампы", "Лампы накаливания", "Галогенные лампы", "Флуоресцентные лампы"],
}

# Словарь правильных ответов
correct_answers = {
    "Что из перечисленного является возобновляемым ресурсом?": "Солнечная энергия",
    "Какой вид энергии выделяется при сгорании угля?": "Тепловая энергия",
    "Какой из этих отходов разлагается быстрее всего?": "Бумага",
    "Какая из следующих мер уменьшает загрязнение воздуха?": "Использование общественного транспорта",
    "Какие лампы потребляют меньше всего энергии?": "Светодиодные лампы",
}

# Переменные для отслеживания состояния игры
user_scores = {}
current_questions = {}

# Функция для начала викторины
@bot.message_handler(commands=['start', 'quiz'])
def start_quiz(message):
    user_id = message.from_user.id
    user_scores[user_id] = 0
    current_questions[user_id] = list(questions.keys())
    shuffle(current_questions[user_id])
    bot.send_message(message.chat.id, "Начнем викторину по экологии! 🧑‍🏫")
    ask_question(message)

# Функция для задания вопроса
def ask_question(message):
    user_id = message.from_user.id
    if len(current_questions[user_id]) == 0:
        bot.send_message(message.chat.id, f"Викторина завершена! Вы ответили правильно на {user_scores[user_id]} из 5 вопросов.")
        return
    question = current_questions[user_id].pop(0)
    options = questions[question]
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
    markup.add(*options)
    bot.send_message(message.chat.id, f"Вопрос: {question}", reply_markup=markup)
    bot.register_next_step_handler(message, check_answer, question)

# Функция для проверки ответа
def check_answer(message, question):
    user_id = message.from_user.id
    if message.text == correct_answers[question]:
        user_scores[user_id] += 1
        bot.send_message(message.chat.id, f"Правильно! 👍 Количество правильных ответов: {user_scores[user_id]}")
    else:
        bot.send_message(message.chat.id, f"Неправильно 😢. Правильный ответ: {correct_answers[question]}")
    ask_question(message)  # Следующий вопрос

# Запуск бота
bot.polling(none_stop=True)
