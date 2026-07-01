"""Test config for aiopegelonline."""

from __future__ import annotations

import json
from collections.abc import AsyncGenerator, Callable, Coroutine
from typing import Any

import aiohttp
import pytest
from aiointercept import CallbackResult, aiointercept

from aiopegelonline import PegelOnline
from aiopegelonline.const import BASE_URL

from .const import MOCK_DATA, MOCK_STATION_DATA_DRESDEN


@pytest.fixture(name="mock_aiointercept")
async def aiointercept_fixture() -> AsyncGenerator[aiointercept, None]:
    """Mock a web request and provide a response."""
    async with aiointercept(mock_external_urls=True) as m:
        yield m


@pytest.fixture(name="mock_pegelonline")
async def pegelonline_fixture() -> AsyncGenerator[PegelOnline, Any]:
    """Return PegelOnline session."""
    session = aiohttp.ClientSession()
    api = PegelOnline(session)
    yield api
    await session.close()


@pytest.fixture
def mock_pegelonline_with_data(
    mock_aiointercept: aiointercept, mock_pegelonline: PegelOnline
) -> Callable[[], Coroutine[Any, Any, PegelOnline]]:
    """Comfort fixture to initialize pegelonline session."""

    async def data_to_pegelonline() -> PegelOnline:
        """Initialize PegelOnline session."""
        for path, data in MOCK_DATA.items():
            mock_aiointercept.get(
                f"{BASE_URL}/{path}",
                status=data["status"],
                body=json.dumps(data["body"]),
                exception=data.get("exception"),
            )
        return mock_pegelonline

    return data_to_pegelonline


@pytest.fixture
def mock_pegelonline_with_cached_data(
    mock_aiointercept: aiointercept, mock_pegelonline: PegelOnline
) -> Callable[[], Coroutine[Any, Any, PegelOnline]]:
    """Comfort fixture to initialize pegelonline session with cached data."""

    def cache_response(_, **kwargs) -> CallbackResult:
        etag = "etag_station_dresden"
        if (headers := kwargs.get("headers")) and headers.get("If-None-Match") == etag:
            return CallbackResult(status=304, body="", headers={"Etag": etag})
        return CallbackResult(
            status=200,
            body=json.dumps(MOCK_STATION_DATA_DRESDEN),
            headers={"Etag": etag},
        )

    async def data_to_pegelonline() -> PegelOnline:
        """Initialize PegelOnline session."""
        query = f"{BASE_URL}/stations/70272185-xxxx-xxxx-xxxx-43bea330dcae.json?prettyprint=false"
        mock_aiointercept.get(query, callback=cache_response, repeat=True)
        return mock_pegelonline

    return data_to_pegelonline
