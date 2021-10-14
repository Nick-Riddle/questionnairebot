def check_name(name):
    if not name.isalpha():
        return 'Вы ввели не строку...'
    elif not 2 < len(name) < 20:
        return 'Строка должна содержать в себе не более 20 и не менее 2 символов...'


def check_age(age):
    if not age.isdigit():
        return 'Вы ввели не число...'
    elif not 2 < int(age) < 102:
        return 'Вам должно быть от 2-102...'


def check_sex(answer):
    if answer not in ('Мужской', 'Женский', 'Назад'):
        return 'Вы не можете ввести другое значение...'
