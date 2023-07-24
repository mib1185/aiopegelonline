"""Test config for aiopegelonline."""
from __future__ import annotations

import json

import aiohttp
import pytest
from aioresponses import aioresponses

from aiopegelonline import PegelOnline
from aiopegelonline.const import BASE_URL

from .const import MOCK_DATA


@pytest.fixture()
def mock_pegelonline():
    """Fixture that the PegelOnline is used with mocked response."""
    with aioresponses() as mock_resp:
        for path, data in MOCK_DATA.items():
            mock_resp.get(
                f"{BASE_URL}/{path}",
                status=data["status"],
                body=json.dumps(data["body"]),
                exception=data.get("exception"),
            )
        yield PegelOnline(aiohttp.ClientSession())
