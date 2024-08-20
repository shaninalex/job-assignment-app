import random


def generate_code(length: int):
    if length <= 0:
        length = 6
    lower_bound = 10 ** (length - 1)
    upper_bound = 10**length - 1
    return f"{random.randint(lower_bound, upper_bound)}"
