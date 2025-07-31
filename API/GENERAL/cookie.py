import random
def generate_cookie():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=64))