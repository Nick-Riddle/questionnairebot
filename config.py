from telebot import types

TOKEN = '2077362215:AAFoob8v4os8AaudWomiUZwPwnKKHAF7xAc'

APP_NAME = 'questionnairebot'

STATES = {
    'state_1': 'Имя',
    'state_2': 'Возраст',
    'state_3': 'Пол',
    'state_4': 'Меню',
    'state_5': 'Инфа',
    'state_6': 'Настройки',
    'state_7': 'Смена имени',
    'state_8': 'Смена возраста',
    'state_9': 'Смена пола',
}


def generate_keyboard(*answer):
    keyboard = types.ReplyKeyboardMarkup(
        one_time_keyboard=True, resize_keyboard=True)
    for item in answer:
        button = types.KeyboardButton(item)
        keyboard.add(button)
    return keyboard
