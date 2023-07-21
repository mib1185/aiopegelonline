"""Constants for aiopegelonline."""
import asyncio
import logging

import aiohttp

LOGGER = logging.getLogger(__package__)

BASE_URL = "https://www.pegelonline.wsv.de/webservices/rest-api/v2"

REQUEST_TIMEOUT = 10

CONNECT_ERRORS = (
    aiohttp.ClientError,
    asyncio.TimeoutError,
    OSError,
)
