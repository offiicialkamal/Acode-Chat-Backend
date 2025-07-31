import random 
def generate_token():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=32))
