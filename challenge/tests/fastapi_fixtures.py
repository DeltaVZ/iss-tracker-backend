from datetime import datetime
from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient

from challenge.database.models.models import IssPosition
from challenge.database.models.visibility import Visibility

SAMPLE_ISS_POSITION = IssPosition(name='iss', satellite_id=25544, latitude=3.7993878441372, longitude=100.21269424675,
                                  altitude=418.710774125, velocity=27581.144139331, visibility=Visibility.DAYLIGHT,
                                  footprint=4500.8986337084, timestamp=1699658022, daynum=2460259.4678472,
                                  solar_lat=-17.276144046636, solar_lon=187.56023046706, units='kilometers')

SAMPLE_TIME_WINDOWS = [(datetime.fromtimestamp(1699658022), datetime.fromtimestamp(1699659022)),
                       (datetime.fromtimestamp(1699662022), datetime.fromtimestamp(1699663022))]


def override_get_db():
    db = Mock()
    yield db


@pytest.fixture
def client():
    from challenge.routers.iss_router import _get_db
    from challenge.fastapi_main import app
    client = TestClient(app)
    app.dependency_overrides[_get_db] = override_get_db
    return client


@pytest.fixture
def mock_latest_iss_position(mocker):
    mocker.patch('challenge.routers.iss_router.get_latest_iss_position',
                 return_value=SAMPLE_ISS_POSITION)
    return SAMPLE_ISS_POSITION


@pytest.fixture
def mock_iss_positions(mocker):
    return mocker.patch('challenge.routers.iss_router.get_iss_positions')


@pytest.fixture
def mock_daylight_time_windows(mocker):
    mocker.patch('challenge.routers.iss_router.get_daylight_time_windows',
                 return_value=SAMPLE_TIME_WINDOWS)
    return SAMPLE_TIME_WINDOWS


@pytest.fixture
def mock_set_up_db(mocker):
    return mocker.patch('challenge.utils.fastapi.fastapi_utils.set_up_db')


@pytest.fixture
def mock_lifespan_db(mocker):
    return mocker.patch('challenge.utils.fastapi.fastapi_utils.get_lifespan_db')
