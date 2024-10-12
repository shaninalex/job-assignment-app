import random
import string


def generate_numeric_code(length: int) -> str:
    if length <= 0:
        length = 6
    lower_bound = 10 ** (length - 1)
    upper_bound = 10**length - 1
    return f"{random.randint(lower_bound, upper_bound)}"


def generate_string_code(length: int) -> str:
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
