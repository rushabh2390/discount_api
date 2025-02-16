import random
import string
from databases.database import data

def generate_discount_code():
    length = random.randint(8, 12)
    random_string = ''.join(random.choices(
        string.ascii_letters + string.digits, k=length))
    data.discount_codes[random_string] = 0.10 # default making 10 percentage
    return random_string