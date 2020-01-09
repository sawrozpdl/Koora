import random
import string


def string(size):
    return ''.join([
        random.choice(
            string.ascii_letters + string.digits
        ) for n in range(size)
    ])
 
def number(size):
    return 0