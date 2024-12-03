from datetime import datetime
from typing import List

from app.models import OpeningHour, OpeningHourType


def format_hour(time: datetime) -> str:
    """
    Formats the datetime value into expected 12-hour clock format

    :param time: datetime value representing the provided timestamp
    :return:
    """
    if time.minute != 0:
        return time.strftime("%-I:%M %p")
    return time.strftime("%-I %p")


def is_restaurant_closed(opening_hours: List[OpeningHour]) -> bool:
    """
    Checks if restaurant is closed for the whole day

    :param opening_hours: list of OpeningHour models
    :return:
    """
    return not opening_hours


def is_first_opening_hour_type_close(opening_hours: List[OpeningHour]) -> bool:
    """
    Checks if the day starts with a close type, i.e. the first opening hour is checked against its type

    :param opening_hours: list of OpeningHour models
    :return:
    """
    first_opening_hour = opening_hours[0]
    return first_opening_hour.type == OpeningHourType.close


def is_opening_hour_type_open(opening_hour: OpeningHour) -> bool:
    """
    Checks if the opening hour type is open

    :param opening_hour: OpeningHour model
    :return:
    """
    return opening_hour.type == OpeningHourType.open
