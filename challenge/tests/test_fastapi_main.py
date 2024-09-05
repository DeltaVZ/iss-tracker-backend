import pytest

from challenge.tests.fastapi_fixtures import client, mock_set_up_db


def test_read_main(mock_set_up_db, client):
    """
    Test for read_main
    :param mock_set_up_db: the mock for the set_up db method
    :param client: the client to send requests with
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to the ISS Tracker challenge!"}
