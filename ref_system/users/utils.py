import random


def create_confirmation_code():
    return random.randint(1000, 9999)


def generate_referal_code():
    letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    digits = '0123456789'
    return ''.join(random.choice(letters + digits) for _ in range(6))
