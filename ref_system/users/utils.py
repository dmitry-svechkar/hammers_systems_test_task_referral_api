import random


def create_confirmation_code():
    """ Простая функция, генерирующая рандомный 4 значный код. """
    return random.randint(1000, 9999)


def generate_referal_code():
    """
    Простая функция,
    генерирующая рандомный 6 значный код из букв и цифр.
    """
    letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    digits = '0123456789'
    return ''.join(random.choice(letters + digits) for _ in range(6))
