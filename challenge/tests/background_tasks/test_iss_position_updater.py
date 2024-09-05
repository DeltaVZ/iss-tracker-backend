import asyncio
from unittest.mock import Mock

import pytest

from challenge.background_tasks.iss_position_updater import IssPositionUpdater
from challenge.database.schemas import IssPosition

SAMPLE_ISS_POSITION_JSON = {"name": "iss", "id": 25544, "latitude": 30.935867918778, "longitude": -110.64276858065,
                            "altitude": 420.90492502545, "velocity": 27584.456083536, "visibility": "eclipsed",
                            "footprint": 4512.0644504846, "timestamp": 1699672660, "daynum": 2460259.6372685,
                            "solar_lat": -17.323258246255, "solar_lon": 126.57295351206, "units": "kilometers"}


@pytest.fixture
def iss_position_updater():
    return IssPositionUpdater(Mock(), {'User-Agent': 'test'}, 1, "fake_url", None)


@pytest.fixture
def mock_aioschedule(mocker) -> dict:
    return {'run_pending': mocker.patch('aioschedule.run_pending'), 'every': mocker.patch('aioschedule.every')}


@pytest.fixture
def mock_update_iss_position(mocker):
    return mocker.patch.object(IssPositionUpdater, 'update_iss_position')


@pytest.fixture
def mock_get_iss_position_from_api(mocker):
    return mocker.patch('challenge.background_tasks.iss_position_updater.get',
                        return_value=SAMPLE_ISS_POSITION_JSON)


@pytest.fixture
def mock_add_iss_position(mocker):
    return mocker.patch('challenge.background_tasks.iss_position_updater.add_iss_position')


@pytest.mark.asyncio
async def test_run_iss_update_position_schedule(mock_aioschedule, mock_update_iss_position, iss_position_updater):
    """
    Tests run_iss_update_position_schedule

    :param mock_aioschedule: the dict of mocks related to aioschedule
    :param mock_update_iss_position: the mock update_iss_position method
    :param iss_position_updater: the IssPositionUpdater
    """
    task = asyncio.create_task(
        iss_position_updater.run_iss_update_position_schedule())
    await asyncio.sleep(0.01)
    mock_aioschedule['run_pending'].assert_called()
    mock_aioschedule['every'].assert_called_with(
        iss_position_updater.wait_time)
    mock_aioschedule['every'].return_value.seconds.do.assert_called_with(
        mock_update_iss_position)
    mock_update_iss_position.assert_called_once()
    task.cancel()


@pytest.mark.asyncio
async def test_update_iss_position(iss_position_updater, mock_get_iss_position_from_api, mock_add_iss_position):
    """
    Tests update_iss_position

    :param iss_position_updater: the IssPositionUpdater
    :param mock_get_iss_position_from_api: the mocked get method
    :param mock_add_iss_position: the mocked add_iss_position method
    """
    await iss_position_updater.update_iss_position()
    mock_get_iss_position_from_api.assert_called_with(iss_position_updater.iss_position_url,
                                                      iss_position_updater._session)
    mock_add_iss_position.assert_called_with(iss_position_updater.db,
                                             IssPosition.from_json(SAMPLE_ISS_POSITION_JSON))
