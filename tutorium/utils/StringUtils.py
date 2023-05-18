import random
import string


def random_string(length):
    letters = string.ascii_letters + string.digits
    random_string = "".join(random.choices(letters, k=length))
    return random_string
