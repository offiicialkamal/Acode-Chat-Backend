import random
import string
def create_cookie():
    return 'MESSANGER__' + ''.join(random.choices(string.ascii_letters + string.digits, k=64))
