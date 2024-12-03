from datetime import datetime
from enum import Enum
from typing import Dict, List

from pydantic import BaseModel, validator


class DayOfWeek(str, Enum):
    monday = "monday"
    tuesday = "tuesday"
    wednesday = "wednesday"
    thursday = "thursday"
    friday = "friday"
    saturday = "saturday"
    sunday = "sunday"


class OpeningHourType(str, Enum):
    open = "open"
    close = "close"


class OpeningHour(BaseModel):
    type: OpeningHourType
    value: datetime

    @validator("value", pre=True)
    def time_value_validate(cls, value: int) -> datetime:
        if not isinstance(value, int):
            raise ValueError(f"{value} should be an integer")
        if value > 86399:
            raise ValueError(f"{value} is bigger than max allowed timestamp")
        return datetime.utcfromtimestamp(value)


class OpeningHours(BaseModel):
    __root__: Dict[DayOfWeek, List[OpeningHour]]
