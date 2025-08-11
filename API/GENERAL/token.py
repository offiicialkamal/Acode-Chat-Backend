import string
import random
def create_token():
    return 'MESS__TOK__'+''.join(random.choices(string.ascii_letters + string.digits, k=32))
