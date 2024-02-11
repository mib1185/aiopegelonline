"""Test config for aiopegelonline."""
from __future__ import annotations

import json

import aiohttp
import pytest
from aioresponses import aioresponses

from aiopegelonline import PegelOnline
from aiopegelonline.const import BASE_URL

from .const import MOCK_DATA


@pytest.fixture
def mock_aioresponse():
    """Mock a web request and provide a response."""
    with aioresponses() as m:
        yield m

@pytest.fixture
async def mock_pegelonline():
    """Return PegelOnline session."""
    session = aiohttp.ClientSession()
    api = PegelOnline(session)
    yield api
    await session.close()

@pytest.fixture
def mock_pegelonline_with_data(mock_aioresponse, mock_pegelonline):
    """Comfort fixture to initialize deCONZ session."""

    async def data_to_pegelonline() -> PegelOnline:
        """Initialize PegelOnline session."""
        for path, data in MOCK_DATA.items():
            mock_aioresponse.get(
                f"{BASE_URL}/{path}",
                status=data["status"],
                body=json.dumps(data["body"]),
                exception=data.get("exception"),
            )
        return mock_pegelonline

    return data_to_pegelonline
