import logging
from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from starlette.requests import Request

from challenge.database.database import SessionLocal
from challenge.database.iss_crud import get_latest_iss_position, get_iss_positions
from challenge.database.models.models import IssPosition
from challenge.utils.fastapi.fastapi_utils import limiter, get_config_utils
from challenge.utils.operations.time_windows_utils import get_daylight_time_windows

router = APIRouter(prefix="/iss", tags=["iss"])
logger = logging.getLogger(__name__)
iss_router_rate_limit = get_config_utils().get_iss_router_rate_limit()


def _get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _get_time_window_dict(time_window: tuple) -> dict:
    return {'start_time': time_window[0], 'end_time': time_window[1]}


def _get_time_windows(iss_positions: list[IssPosition]) -> list[dict]:
    return [_get_time_window_dict(time_window) for time_window in
            get_daylight_time_windows(iss_positions)]


def _get_brief_position_response(latest_iss_position: IssPosition) -> dict:
    return {'latitude': latest_iss_position.latitude, 'longitude': latest_iss_position.longitude,
            'timestamp': latest_iss_position.timestamp}


@router.get("/sun")
@limiter.limit(iss_router_rate_limit)
async def read_sun(request: Request, db: Session = Depends(_get_db),
                   start_time: datetime = Query(None,
                                                description="Start timestamp for "
                                                            "the exposed to sun time "
                                                            "windows. By default, "
                                                            "it will be the time at "
                                                            "which the query is "
                                                            "executed minus one day"),
                   end_time: datetime = Query(None,
                                              description="End timestamp for the exposed to "
                                                          "SUN time windows. By default,"
                                                          "it will be the time at which the"
                                                          "query is executed"),
                   time_window_size: int = Query(86400,
                                                 description="The size of the time window to consider to get "
                                                             "IssPositions: the given value will be subracted from "
                                                             "end_time to calculate the start_time. It's ignored if "
                                                             "start_time is provided")):
    """
    Provides a List of time windows in which the ISS was exposed to the SUN
    :param start_time: start time for the exposed to sun time windows
    :param end_time: end time for the exposed to sun time windows
    :param time_window_size: used if start_time is not provided. It indicates the time in seconds to subtract from end_time to calculate the start_time
    :param db: the DB where the IssPosition is stored
    :return: a List of time windows in which the ISS was exposed to the SUN
    """

    iss_positions = get_iss_positions(db, start_time, end_time,
                                      time_window_size)
    return _get_time_windows(iss_positions)


@router.get("/position")
@limiter.limit(iss_router_rate_limit)
async def read_position(request: Request, db: Session = Depends(_get_db),
                        detailed: bool = Query(False, description="Return a detailed IssPosition")):
    """
    Gets the latest position of the ISS
    :param db: the DB where the IssPosition is stored
    :param detailed: if false, it will only return latitude, longitude and timestamp of the latest IssPosition
    :return: the latest IssPosition
    """
    latest_iss_position = get_latest_iss_position(db)
    response = {}
    if latest_iss_position:
        if detailed:
            response = latest_iss_position
        else:
            response = _get_brief_position_response(latest_iss_position)
    return response
