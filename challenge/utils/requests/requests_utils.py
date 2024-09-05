import asyncio
import logging

import aiohttp
from aiohttp import ClientSession

logger = logging.getLogger(__name__)
MAX_RETRIES = 3


async def get(url: str, session: ClientSession, retries: int = 0) -> dict:
    """
    Simply make an HTTP request to the given URL with a new session
    :param url: the url of the website to send an HTTP request to
    :param session: the ClientSession
    :param retries: the number of retries that have been executed
    :return: the response
    """
    logger.debug('Requesting %s', url)
    try:
        async with session.get(url) as r:
            return await r.json()
    except aiohttp.ClientError as e:
        logger.warning('Could not get %s. Current retry: %s. Maximum allowed retries: %s}', url, retries, MAX_RETRIES)
        await asyncio.sleep(0.5)
        if retries < MAX_RETRIES:
            retries += 1
            return await get(url, session, retries)
        logger.error(
            'Could not get %s. Maximum number of retries (%s) exceeded. Will retry at next scheduled '
            'time. Error: %s', url, MAX_RETRIES, e)
    except Exception as e:
        logger.error('Could not get %s. Will retry at next scheduled time. Error: %s', url, e)
