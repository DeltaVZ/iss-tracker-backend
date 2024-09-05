import datetime
from unittest import mock

import pytest
from fastapi.encoders import jsonable_encoder

from challenge.tests.fastapi_fixtures import client, mock_set_up_db, mock_latest_iss_position, \
    mock_iss_positions, mock_daylight_time_windows


@pytest.fixture
def disabled_limiter():
    # Disable API limits in case they are enabled
    from challenge.utils.fastapi.fastapi_utils import limiter
    limiter.enabled = False
    return limiter


def test_iss_position(mock_set_up_db, client, mock_latest_iss_position, disabled_limiter):
    """
    Test for read_position

    :param mock_set_up_db: the mock for the set_up db method
    :param client: the client to send requests with
    :param mock_latest_iss_position: the latest iss position that is set to be returned
    :param limiter the disabled limiter
    """
    base_endpoint = '/iss/position'

    # 1: Testing the simple /iss/position endpoint
    response = client.get(base_endpoint)
    assert response.status_code == 200
    assert response.json() == {'latitude': mock_latest_iss_position.latitude,
                               'longitude': mock_latest_iss_position.longitude,
                               'timestamp': mock_latest_iss_position.timestamp}

    # 2: Testing the /iss/position endpoint with detailed as true
    response = client.get(f'{base_endpoint}?detailed=true')
    assert response.status_code == 200
    assert response.json() == jsonable_encoder(mock_latest_iss_position)


def test_iss_sun(mock_set_up_db, client, mock_iss_positions, mock_daylight_time_windows, disabled_limiter):
    """
    Test for read_sun

    :param mock_set_up_db: the mock for the set_up db method
    :param client: the client to send requests with
    :param mock_iss_positions: the mocked list of IssPosition
    :param mock_daylight_time_windows: the List of TimeWindow expected to ber returned
    :param limiter the disabled limiter
    """

    base_endpoint = '/iss/sun'

    # 1: Simple request
    response = client.get(base_endpoint)
    assert response.status_code == 200
    assert response.json() == jsonable_encoder(
        [{'start_time': time_window[0], 'end_time': time_window[1]} for time_window in
         mock_daylight_time_windows])
    mock_iss_positions.assert_called_once_with(mock.ANY, None, None, 86400)

    # 2: Request with start and end time
    start_time = '2023-11-11T01:00:00'
    end_time = '2023-11-14T03:42:08'
    response = client.get(
        f'{base_endpoint}?start_time={start_time}&end_time={end_time}')
    assert response.status_code == 200
    mock_iss_positions.assert_called_with(mock.ANY, datetime.datetime.fromisoformat(start_time),
                                          datetime.datetime.fromisoformat(
                                              end_time),
                                          86400)

    # 3: Request with time_window_size
    time_window_size = 100
    response = client.get(
        f'{base_endpoint}?time_window_size={time_window_size}')
    assert response.status_code == 200
    mock_iss_positions.assert_called_with(mock.ANY, None,
                                          None,
                                          time_window_size)
