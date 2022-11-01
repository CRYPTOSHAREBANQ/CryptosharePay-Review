import random
import string

def generate_pin(lenght = 6):
        return ''.join(random.choice(string.digits) for i in range(lenght))