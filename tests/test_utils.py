from datetime import datetime

import pytest

from app.models import OpeningHour
from app.utils import (
    format_hour,
    is_first_opening_hour_type_close,
    is_opening_hour_type_open,
    is_restaurant_closed,
)


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (datetime.utcfromtimestamp(3600), "1 AM"),
        (datetime.utcfromtimestamp(1000), "12:16 AM"),
    ],
)
def test_format_hour(test_input, expected):
    result = format_hour(test_input)
    assert result == expected


@pytest.mark.parametrize(
    "test_input,expected", [([], True), ([OpeningHour(type="open", value=3600)], False)]
)
def test_is_restaurant_closed(test_input, expected):
    result = is_restaurant_closed(test_input)
    assert result == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (
            [
                OpeningHour(type="open", value=3600),
                OpeningHour(type="close", value=3600),
            ],
            False,
        ),
        (
            [
                OpeningHour(type="close", value=3600),
                OpeningHour(type="open", value=3600),
            ],
            True,
        ),
    ],
)
def test_is_first_opening_hour_type_close(test_input, expected):
    result = is_first_opening_hour_type_close(test_input)
    assert result == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (OpeningHour(type="open", value=3600), True),
        (OpeningHour(type="close", value=3600), False),
    ],
)
def test_is_opening_hour_type_open(test_input, expected):
    result = is_opening_hour_type_open(test_input)
    assert result == expected
