import random
import string
import datetime

def generate_pin(lenght = 6):
    return ''.join(random.choice(string.digits) for i in range(lenght))

def date_for_weekday(day: int):
    today = datetime.datetime.today()

    weekday = today.weekday()
    return today + datetime.timedelta(days=day - weekday)

        