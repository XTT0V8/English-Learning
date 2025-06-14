import telebot
from time import sleep
import random

Token ="8176947440:AAHtft8mF7muoGe73e5FIN8Na_2FY0Z01-E"
bot = telebot.TeleBot(Token)

# Пример словаря слов: русское → английское
words = {
    "кошка": "cat",
    "собака": "dog",
    "яблоко": "apple",
    "дом": "house",
    "книга": "book",
    "вода": "water",
    "окно" : "window",
    "дверь" : "door",
    "гриб" : "mushroom",
    "карандаш" : "pencil",
    "ручка" : "pen",
    "линейка" : "ruller",
    "обновление" : "update",
    "бежать" : "run",
    "читать" : "read",
    "смотреть фильм" : "watch the film",
    "фильм" : "film",
    "английский" : "english",
    "язык" : "language",
    "ангийский язык" : "english language",
}

# Храним текущее слово для пользователя
user_words = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет, я бот для изучения английского языка!")
    bot.send_message(message.chat.id, "Давай начнём занятие")


@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(message.chat.id, "/start - запуск бота\n" \
                                      "/help - список команд\n" \
                                      "/remove - перезапустить бота\n" \
                                      "/start_learning - начать изучение слов\n" \
                                      "/stop_learning - остановить изучение\n" \
                                      "/help_with_word - помощь со словом")


@bot.message_handler(commands=['stop_learning'])
def stop_learning(message):
    if message.chat.id in user_words:
        del user_words[message.chat.id]
        bot.send_message(message.chat.id, "🛑 Обучение остановлено. Напиши /start_learning, чтобы начать заново.")
    else:
        bot.send_message(message.chat.id, "Сейчас обучение не запущено.")


@bot.message_handler(commands=['start_learning'])
def start_learning(message):
    word = random.choice(list(words.keys()))
    user_words[message.chat.id] = word
    bot.send_message(message.chat.id, f"Как будет по-английски: *{word}*?", parse_mode='Markdown')

@bot.message_handler(commands=['help_with_word'])
def help_with_word(message):
    word = user_words.get(message.chat.id)
    if word:
        translation = words[word]
        bot.send_message(message.chat.id, f"Подсказка: {word} = {translation}")
    else:
        bot.send_message(message.chat.id, "Сначала начни занятие с /start_learning")

@bot.message_handler(func=lambda message: True)
def check_answer(message):
    word = user_words.get(message.chat.id)
    if word:
        correct = words[word].lower()
        answer = message.text.strip().lower()
        if answer == correct:
            bot.send_message(message.chat.id, "✅ Правильно! Молодец!")
        else:
            bot.send_message(message.chat.id, f"❌ Неправильно. Правильный ответ: {correct}")
        # Новое слово после проверки
        word = random.choice(list(words.keys()))
        user_words[message.chat.id] = word
        bot.send_message(message.chat.id, f"Как будет по-английски: *{word}*?", parse_mode='Markdown')
    else:
        bot.send_message(message.chat.id, "Чтобы начать учёбу, нажми /start_learning")

bot.polling()
