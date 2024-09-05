import asyncio
import logging
import aioschedule
import aiohttp

from challenge.database.database import SessionLocal
from challenge.database.iss_crud import add_iss_position
from challenge.database.schemas import IssPosition
from challenge.utils.config.config_utils import ConfigUtils
from challenge.utils.requests.requests_utils import get

logger = logging.getLogger(__name__)


class IssPositionUpdater:
    """
    The ISS Position updater
    """
    __slots__ = ['db', '_session', 'headers', 'wait_time', 'iss_position_url', 'stop_schedule']

    def __init__(self, db: SessionLocal, headers: dict = None, wait_time: int = -1, iss_position_url: str = None,
                 config_utils: ConfigUtils = ConfigUtils()):

        """
        :param db: the db
        :param headers: the headers to be used for the GET request to get the ISS position
        :param wait_time: the wait time between requests
        :param iss_position_url: the URL to send a GET request to in order to get the ISS position
        :param config_utils the ConfigUtils object
        """
        self._session = None
        self.headers = headers if headers else self._get_default_headers(config_utils)
        self.iss_position_url = iss_position_url if iss_position_url else config_utils.get_iss_position_url()
        self.wait_time = wait_time if self._is_wait_time_valid(wait_time) else config_utils.get_wait_time()
        self.db = db
        self.stop_schedule = False

    async def run_iss_update_position_schedule(self) -> None:
        """
        Runs update_iss_position() once and then schedules it to run every 20 seconds
        """
        async with aiohttp.ClientSession(headers=self.headers) as self._session:
            await self.update_iss_position()
            aioschedule.every(self.wait_time).seconds.do(self.update_iss_position)
            while not self.stop_schedule:
                await aioschedule.run_pending()
                await asyncio.sleep(0.05)

    async def update_iss_position(self) -> None:
        """
        Requests an external API for the ISS position and updates the DB with the latest ISS position
        """
        json = await get(self.iss_position_url, self._session)
        if json:
            iss_position = IssPosition.from_json(json)
            add_iss_position(self.db, iss_position)
            logger.debug("Updated ISS Position: %s", json)

    @staticmethod
    def _get_default_headers(config_utils: ConfigUtils) -> dict:
        return {"User-Agent": config_utils.get_user_agent()}

    @staticmethod
    def _is_wait_time_valid(wait_time) -> bool:
        return type(wait_time) is int and wait_time > 0
