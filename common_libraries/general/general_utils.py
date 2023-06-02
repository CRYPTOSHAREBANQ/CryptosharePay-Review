from dateutil.relativedelta import relativedelta


from common_libraries.constants.automated import AVAILABLE_FRECUENCIES, AVAILABLE_SHEDULED_DAYS

import random
import string
import datetime

def generate_pin(length = 6):
    return ''.join(random.choice(string.digits) for i in range(length))

def generate_password(length = 12):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

def date_for_weekday(day: int):
    today = datetime.datetime.today()

    weekday = today.weekday()
    return today + datetime.timedelta(days=day - weekday)

def get_next_event_datetime(frecuency, scheduled_day):
    now_datetime = datetime.datetime.now()

    if frecuency == "WEEKLY":
        current_weekday_datetime = date_for_weekday(AVAILABLE_SHEDULED_DAYS["WEEKLY"][scheduled_day])

        if now_datetime > current_weekday_datetime:
            next_event_datetime = current_weekday_datetime + relativedelta(weeks = 1)
        else:
            next_event_datetime = current_weekday_datetime
    elif frecuency == "MONTHLY":
        month_day_datetime = datetime.datetime.now().replace(day = scheduled_day)

        if now_datetime > month_day_datetime:
            next_event_datetime = month_day_datetime + relativedelta(months = 1)
        else:
            next_event_datetime = month_day_datetime
    
    return next_event_datetime