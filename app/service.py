from typing import Final, List

from app.models import DayOfWeek, OpeningHours
from app.utils import (
    format_hour,
    is_first_opening_hour_type_close,
    is_opening_hour_type_open,
    is_restaurant_closed,
)

OPENING_HOUR_SEPARATOR: Final[str] = " - "
OPEN_CLOSE_SLOT_SEPARATOR: Final[str] = ", "


class OpeningHourLine:
    """
    A representation of each opening hours line in textual format
    """

    def __init__(self, day_of_week: DayOfWeek) -> None:
        self._line = f"{day_of_week.value.title()}: "

    def add_closed(self) -> None:
        self._line = f"{self._line}Closed"

    def add_formatted_hour_with_open_type(self, formatted_hour: str) -> None:
        self._line = f"{self._line}{formatted_hour}{OPENING_HOUR_SEPARATOR}"

    def add_formatted_hour_with_close_type(self, formatted_hour: str) -> None:
        self._line = f"{self._line}{formatted_hour}{OPEN_CLOSE_SLOT_SEPARATOR}"

    def __str__(self) -> str:
        return self._line.rstrip(", ")


class OpeningHoursOutput:
    """
    A representation of the collection of opening hour lines
    """

    def __init__(self) -> None:
        self.lines: List[OpeningHourLine] = []

    def add_line(self, line: OpeningHourLine) -> None:
        self.lines.append(line)

    def pop_line(self) -> OpeningHourLine:
        return self.lines.pop()

    def flush(self) -> str:
        return "\n".join(map(str, self.lines))


def convert_to_text_output(opening_hours: OpeningHours) -> str:
    """
    Returns the textual output in compliance with the format mentioned in documentation, see README.md

    :param opening_hours: Input format represented as a model
    :return: Output format as a text
    """
    opening_hours_output = OpeningHoursOutput()

    for day_of_week, day_opening_hours in opening_hours.__root__.items():
        line = OpeningHourLine(day_of_week)

        if is_restaurant_closed(day_opening_hours):
            line.add_closed()
            opening_hours_output.add_line(line)
            continue

        if is_first_opening_hour_type_close(day_opening_hours):
            first_opening_hour = day_opening_hours.pop(0)
            previous_line = opening_hours_output.pop_line()

            formatted_hour = format_hour(first_opening_hour.value)
            previous_line.add_formatted_hour_with_close_type(formatted_hour)
            opening_hours_output.add_line(previous_line)

        for opening_hour in day_opening_hours:

            if is_opening_hour_type_open(opening_hour):
                formatted_hour = format_hour(opening_hour.value)
                line.add_formatted_hour_with_open_type(formatted_hour)
                continue

            formatted_hour = format_hour(opening_hour.value)
            line.add_formatted_hour_with_close_type(formatted_hour)

        opening_hours_output.add_line(line)

    return opening_hours_output.flush()
