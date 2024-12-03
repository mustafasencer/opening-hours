from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_welcome():
    response = client.get("/")
    assert response.status_code == 200
    assert (
        response.text
        == "Welcome to Opening Hours Service!\nFor more info please check /docs endpoint"
    )


def test_convert_hour_with_success():
    response = client.post(
        "/v1/ConvertOpeningHours/",
        json={
            "monday": [
                {"type": "open", "value": 1000},
                {"type": "close", "value": 2000},
            ]
        },
    )
    assert response.status_code == 200


def test_convert_hour_with_incorrect_input():
    response = client.post(
        "/v1/ConvertOpeningHours/", json={"monday": [{"type": "open", "value": "100"}]}
    )
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "100 should be an integer"


def test_convert_hour_with_invalid_day_of_week():
    response = client.post(
        "/v1/ConvertOpeningHours/",
        json={"invalid_key": [{"type": "open", "value": 100}]},
    )
    assert response.status_code == 422
    assert (
        response.json()["detail"][0]["msg"]
        == "value is not a valid enumeration member; permitted: 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'"
    )


def test_convert_hour_with_invalid_opening_hour_value():
    response = client.post(
        "/v1/ConvertOpeningHours/",
        json={"monday": [{"type": "open", "value": 1000000}]},
    )
    assert response.status_code == 422
    assert (
        response.json()["detail"][0]["msg"]
        == "1000000 is bigger than max allowed timestamp"
    )


def test_convert_hour_with_invalid_opening_hour_type():
    response = client.post(
        "/v1/ConvertOpeningHours/",
        json={"monday": [{"type": "invalid", "value": 10000}]},
    )
    assert response.status_code == 422
    assert (
        response.json()["detail"][0]["msg"]
        == "value is not a valid enumeration member; permitted: 'open', 'close'"
    )


def test_convert_hour_with_correct_text_output_format():
    response = client.post(
        "/v1/ConvertOpeningHours/",
        json={
            "tuesday": [
                {"type": "open", "value": 36000},
                {"type": "close", "value": 64800},
            ],
            "thursday": [
                {"type": "open", "value": 37800},
                {"type": "close", "value": 64800},
            ],
            "friday": [{"type": "open", "value": 36000}],
            "saturday": [
                {"type": "close", "value": 3600},
                {"type": "open", "value": 36000},
            ],
            "sunday": [
                {"type": "close", "value": 3600},
                {"type": "open", "value": 43200},
                {"type": "close", "value": 75600},
            ],
        },
    )
    assert response.status_code == 200
    assert (
        response.text
        == "Tuesday: 10 AM - 6 PM\nThursday: 10:30 AM - 6 PM\nFriday: 10 AM - 1 AM\nSaturday: 10 AM - 1 AM\nSunday: 12 PM - 9 PM"
    )


def test_convert_hour_with_multiple_open_and_close_in_a_day():
    response = client.post(
        "/v1/ConvertOpeningHours/",
        json={
            "monday": [
                {"type": "open", "value": 1000},
                {"type": "close", "value": 2000},
                {"type": "open", "value": 3000},
                {"type": "close", "value": 4000},
            ]
        },
    )
    assert response.status_code == 200
    assert response.text == "Monday: 12:16 AM - 12:33 AM, 12:50 AM - 1:06 AM"


def test_convert_hour_with_open_hours_spanning_multiple_days():
    response = client.post(
        "/v1/ConvertOpeningHours/",
        json={
            "friday": [{"type": "open", "value": 64800}],
            "saturday": [
                {"type": "close", "value": 3600},
                {"type": "open", "value": 32400},
                {"type": "close", "value": 39600},
                {"type": "open", "value": 57600},
                {"type": "close", "value": 82800},
            ],
        },
    )
    assert response.status_code == 200
    assert response.text == "Friday: 6 PM - 1 AM\nSaturday: 9 AM - 11 AM, 4 PM - 11 PM"


def test_convert_hour_with_restaurant_closed_the_whole_day():
    response = client.post("/v1/ConvertOpeningHours/", json={"monday": []})
    assert response.status_code == 200
    assert response.text == "Monday: Closed"
