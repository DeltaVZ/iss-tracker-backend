from datetime import datetime, timedelta
from typing import Union

from sqlalchemy import desc, asc
from sqlalchemy.orm import Session

from challenge.database import schemas
from challenge.database.models import models
from challenge.database.models.models import IssPosition


def get_iss_positions(db: Session, start_time: datetime = None, end_time: datetime = None,
                      timedelta_seconds: int = 86400) -> list:
    """
    Gets the iss positions between the given start and end times
    :param db: the DB
    :param start_time: the start time. If None, it'll be now time
    :param end_time: the end time. If None, it'll be now time - the timedelta_seconds
    :param timedelta_seconds: the timedelta to be used to calculate the start time if it is None
    :return: a list of IssPosition
    """
    if not end_time:
        end_time = datetime.now()
    if not start_time:
        start_time = end_time - timedelta(seconds=timedelta_seconds)
    return db.query(models.IssPosition).filter(models.IssPosition.timestamp.between(start_time, end_time)).order_by(
        asc('timestamp')).all()


def get_latest_iss_position(db: Session) -> Union[IssPosition, None]:
    """
    Gets the latest IssPosition in the DB
    :param db: the DB
    :return: the latest IssPosition
    """
    return db.query(models.IssPosition).order_by(desc('timestamp')).first()


def add_iss_position(db: Session, iss_position: schemas.IssPosition):
    """
    Adds the given IssPosition to the DB
    :param db: the DB
    :param iss_position: the IssPosition to add
    :return: the added IssPosition
    """
    db_iss_position = models.IssPosition(**iss_position.model_dump())
    db.add(db_iss_position)
    db.commit()
    db.refresh(db_iss_position)
    return db_iss_position
