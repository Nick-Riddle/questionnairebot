class NotString(Exception):
    def __init__(self, text):
        self.text = text


class TooManyOrLessLetters(Exception):
    def __init__(self, text):
        self.text = text


class TooManyOrLessYears(Exception):
    def __init__(self, text):
        self.text = text


class WrongOption(Exception):
    def __init__(self, text):
        self.text = text


def check_name(name):
    try:
        if not name.isalpha():
            raise NotString('Вы ввели не строку...')
        elif not 2 < len(name) < 20:
            raise TooManyOrLessLetters('Строка должна содержать в себе не более 20 и не менее 2 символов...')
    except NotString as ns:
        return ns
    except TooManyOrLessLetters as tmlt:
        return tmlt


def check_age(age):
    if not age.isdigit():
        return 'Вы ввели не число...'
    elif not 2 < age < 102:
        return 'Вам должно быть от 2-102...'
    else:
        return False
    # try:
    #     age = int(age)
    #     if not 2 < age < 102:
    #         raise TooManyOrLessYears('Вам должно быть от 2-102...')
    # except ValueError:
    #     return 'Вы ввели не число...'
    # except TooManyOrLessYears as tmly:
    #     return tmly


def check_sex(answer):
    try:
        if answer not in ('Мужской', 'Женский', 'Назад'):
            raise WrongOption('Вы не можете ввести другое значение...')
    except WrongOption as wo:
        return wo
