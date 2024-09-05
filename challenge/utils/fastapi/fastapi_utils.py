from slowapi import Limiter
from slowapi.util import get_remote_address

from challenge.database.database import engine, SessionLocal
from challenge.database.models import models
from challenge.utils.config.config_utils import ConfigUtils

limiter = Limiter(key_func=get_remote_address)


def set_up_db() -> None:
    """
    Sets up the DB
    """
    models.Base.metadata.create_all(bind=engine)


def get_lifespan_db() -> SessionLocal:
    """
    Provides the DB to be used for FastAPI's lifespan method
    :return the SessionLocal
    """
    return SessionLocal()


def get_config_utils() -> ConfigUtils:
    """
    Returns a ConfigUtils instance
    :return: a ConfigUtils instance
    """
    return ConfigUtils()
