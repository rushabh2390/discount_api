import random
import string
from databases.database import data

def generate_discount_code(discount_value):
    """_summary_

    Args:
        discount_value (_int_): _disount value_

    Returns:
        _str_: _return discount_code_
    """
    length = random.randint(8, 12)
    random_string = ''.join(random.choices(
        string.ascii_letters + string.digits, k=length))
    data.discount_codes[random_string] = discount_value
    return random_string