import telebot

import config
import db_users
import validators

bot = telebot.TeleBot(token=config.TOKEN)

keyboard_settings = config.generate_keyboard(
    'Сменить имя', 'Сменить возраст', 'Сменить пол', 'Назад')
keyboard_menu = config.generate_keyboard('Инфа про меня', 'Настройки')
keyboard_sex = config.generate_keyboard('Мужской', 'Женский', 'Назад')
keyboard_back = config.generate_keyboard('Назад')


@bot.message_handler(commands=["start"])
def command_start(message):
    db_users.check_and_add_user(message)
    bot.send_message(message.from_user.id, 'Напишите свое имя:')
    db_users.set_new_state(message.from_user.id, config.STATES['state_1'])


@bot.message_handler(
    func=lambda message: db_users.get_current_state(
        message.from_user.id) == config.STATES['state_1'])
def get_user_name(message):
    checking_name = validators.check_name(message.text)
    if checking_name:
        bot.send_message(
            message.from_user.id,
            f'{checking_name}. Попробуйте снова.')
        command_start(message)
    else:
        db_users.cur.execute(
            f"UPDATE user_questionnaire SET name = '{message.text}' WHERE id = {message.from_user.id}")
        db_users.con.commit()
        bot.send_message(
            message.from_user.id,
            'Ваш возраст?:',
            reply_markup=keyboard_back)
        db_users.set_new_state(message.from_user.id, config.STATES['state_2'])


@bot.message_handler(
    func=lambda message: db_users.get_current_state(
        message.from_user.id) == config.STATES['state_2'])
def get_user_age(message):
    checking_age = validators.check_age(message.text)
    if message.text == 'Назад':
        command_start(message)
    elif checking_age:
        bot.send_message(
            message.from_user.id,
            f'{checking_age} Попробуйте снова.')
        come_back_to_name(message)
    else:
        db_users.cur.execute(
            f"UPDATE user_questionnaire SET age = {message.text} WHERE id = {message.from_user.id}")
        db_users.con.commit()
        bot.send_message(
            message.from_user.id,
            'Ваш пол?:',
            reply_markup=keyboard_sex)
        db_users.set_new_state(message.from_user.id, config.STATES['state_3'])


@bot.message_handler(
    func=lambda message: db_users.get_current_state(
        message.from_user.id) == config.STATES['state_3'])
def get_user_sex(message):
    checking_sex = validators.check_sex(message.text)
    if message.text == 'Назад':
        come_back_to_name(message)
    elif checking_sex:
        bot.send_message(
            message.from_user.id,
            f'{checking_sex} Попробуйте снова.')
        come_back_to_age(message)
    else:
        db_users.cur.execute(
            f"UPDATE user_questionnaire SET sex = '{message.text}' WHERE id = {message.from_user.id}")
        db_users.con.commit()
        bot.send_message(
            message.from_user.id,
            'Главное меню:',
            reply_markup=keyboard_menu)
        db_users.set_new_state(message.from_user.id, config.STATES['state_4'])


@bot.message_handler(
    func=lambda message: db_users.get_current_state(
        message.from_user.id) == config.STATES['state_4'])
def menu(message):
    if message.text == 'Инфа про меня':
        db_users.cur.execute(
            f"SELECT name, age, sex FROM user_questionnaire WHERE id = {message.from_user.id}")
        info = db_users.cur.fetchone()
        bot.send_message(
            message.from_user.id,
            f'Ваше имя: {info[0]}\nВаш возраст: {info[1]}\nВаш пол: {info[2]}',
            reply_markup=keyboard_back)
        db_users.set_new_state(message.from_user.id, config.STATES['state_5'])
    elif message.text == 'Настройки':
        bot.send_message(
            message.from_user.id,
            'Настройки:',
            reply_markup=keyboard_settings)
        db_users.set_new_state(message.from_user.id, config.STATES['state_6'])


@bot.message_handler(
    func=lambda message: db_users.get_current_state(
        message.from_user.id) == config.STATES['state_5'])
def back_info(message):
    if message.text == 'Назад':
        come_back_to_sex(message)


@bot.message_handler(
    func=lambda message: db_users.get_current_state(
        message.from_user.id) == config.STATES['state_6'])
def settings(message):
    if message.text == 'Сменить имя':
        bot.send_message(
            message.from_user.id,
            'Введите новое имя:',
            reply_markup=keyboard_back)
        db_users.set_new_state(message.from_user.id, config.STATES['state_7'])
    elif message.text == 'Сменить возраст':
        bot.send_message(
            message.from_user.id,
            'Введите новый возраст:',
            reply_markup=keyboard_back)
        db_users.set_new_state(message.from_user.id, config.STATES['state_8'])
    elif message.text == 'Сменить пол':
        bot.send_message(
            message.from_user.id,
            'Введите новый пол:',
            reply_markup=keyboard_sex)
        db_users.set_new_state(message.from_user.id, config.STATES['state_9'])
    elif message.text == 'Назад':
        come_back_to_sex(message)


@bot.message_handler(
    func=lambda message: db_users.get_current_state(
        message.from_user.id) == config.STATES['state_7'])
def change_user_name(message):
    checking_name = validators.check_name(message.text)
    if message.text == 'Назад':
        db_users.set_new_state(message.from_user.id, config.STATES['state_4'])
        message.text = 'Настройки'
        menu(message)
    elif checking_name:
        bot.send_message(
            message.from_user.id,
            f'{checking_name}. Попробуйте снова.')
        message.text = 'Сменить имя'
        db_users.set_new_state(message.from_user.id, config.STATES['state_6'])
        settings(message)
    else:
        db_users.cur.execute(
            f"UPDATE user_questionnaire SET name = '{message.text}' WHERE id = {message.from_user.id}")
        db_users.con.commit()
        db_users.set_new_state(message.from_user.id, config.STATES['state_4'])
        message.text = 'Настройки'
        menu(message)


@bot.message_handler(
    func=lambda message: db_users.get_current_state(
        message.from_user.id) == config.STATES['state_8'])
def change_user_age(message):
    checking_age = validators.check_age(message.text)
    if message.text == 'Назад':
        db_users.set_new_state(message.from_user.id, config.STATES['state_4'])
        message.text = 'Настройки'
        menu(message)
    elif checking_age:
        bot.send_message(
            message.from_user.id,
            f'{checking_age}. Попробуйте снова.')
        message.text = 'Сменить возраст'
        db_users.set_new_state(message.from_user.id, config.STATES['state_6'])
        settings(message)
    else:
        db_users.cur.execute(
            f"UPDATE user_questionnaire SET age = {message.text} WHERE id = {message.from_user.id}")
        db_users.con.commit()
        db_users.set_new_state(message.from_user.id, config.STATES['state_4'])
        message.text = 'Настройки'
        menu(message)


@bot.message_handler(
    func=lambda message: db_users.get_current_state(
        message.from_user.id) == config.STATES['state_9'])
def change_user_sex(message):
    checking_sex = validators.check_sex(message.text)
    if message.text == 'Назад':
        db_users.set_new_state(message.from_user.id, config.STATES['state_4'])
        message.text = 'Настройки'
        menu(message)
    elif checking_sex:
        bot.send_message(
            message.from_user.id,
            f'{checking_sex}. Попробуйте снова.')
        message.text = 'Сменить пол'
        db_users.set_new_state(message.from_user.id, config.STATES['state_6'])
        settings(message)
    else:
        db_users.cur.execute(
            f"UPDATE user_questionnaire SET sex = '{message.text}' WHERE id = {message.from_user.id}")
        db_users.con.commit()
        db_users.set_new_state(message.from_user.id, config.STATES['state_4'])
        message.text = 'Настройки'
        menu(message)


def come_back_to_name(message):
    db_users.set_new_state(message.from_user.id, config.STATES['state_1'])
    db_users.cur.execute(
        f"SELECT name FROM user_questionnaire WHERE id = {message.from_user.id}")
    name = db_users.cur.fetchone()
    message.text = name[0]
    get_user_name(message)


def come_back_to_age(message):
    db_users.set_new_state(message.from_user.id, config.STATES['state_2'])
    db_users.cur.execute(
        f"SELECT age FROM user_questionnaire WHERE id = {message.from_user.id}")
    age = db_users.cur.fetchone()
    message.text = age[0]
    get_user_age(message)


def come_back_to_sex(message):
    db_users.set_new_state(message.from_user.id, config.STATES['state_3'])
    db_users.cur.execute(
        f"SELECT sex FROM user_questionnaire WHERE id = {message.from_user.id}")
    sex = db_users.cur.fetchone()
    message.text = sex[0]
    get_user_sex(message)
