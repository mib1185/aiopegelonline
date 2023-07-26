"""Pegelonline library."""

from __future__ import annotations

import json

from aiohttp.client import ClientSession

from .const import BASE_URL, CONNECT_ERRORS, LOGGER, REQUEST_TIMEOUT
from .exceptions import PegelonlineDataError
from .models import Station, StationMeasurements


class PegelOnline:
    """Pegelonline api."""

    def __init__(self, aiohttp_session: ClientSession) -> None:
        """Pegelonline api init."""
        self.session: ClientSession = aiohttp_session

    async def _async_do_request(self, url: str, params: dict):
        """Perform an async request."""
        LOGGER.debug("REQUEST url: %s params: %s", url, params)
        try:
            async with self.session.get(
                url, params=params, timeout=REQUEST_TIMEOUT
            ) as resp:
                result = await resp.text()
                LOGGER.debug("RESPONSE status: %s text: %s", resp.status, result)
                result = json.loads(result)
                if resp.status != 200:
                    raise PegelonlineDataError(
                        result.get("status"), result.get("message")
                    )
        except CONNECT_ERRORS as err:
            LOGGER.exception("Error while getting data: %s", err.__class__.__name__)
            raise err

        return result

    async def async_get_all_stations(self) -> dict[str, Station]:
        """Get all stations."""
        stations = await self._async_do_request(
            f"{BASE_URL}/stations.json", {"prettyprint": "false"}
        )

        result = {}
        for station in stations:
            result[station["uuid"]] = Station(station)

        return result

    async def async_get_nearby_stations(
        self, latitude: float, longitude: float, radius: int
    ) -> dict[str, Station]:
        """Get stations within defined radius at given position."""
        stations = await self._async_do_request(
            f"{BASE_URL}/stations.json",
            {
                "prettyprint": "false",
                "latitude": latitude,
                "longitude": longitude,
                "radius": radius,
            },
        )

        result = {}
        for station in stations:
            result[station["uuid"]] = Station(station)

        return result

    async def async_get_station_details(self, uuid: str) -> Station:
        """Get station details."""
        station = await self._async_do_request(
            f"{BASE_URL}/stations/{uuid}.json", {"prettyprint": "false"}
        )

        return Station(station)

    async def async_get_station_measurements(self, uuid: str) -> StationMeasurements:
        """Get all current measurements of a station."""
        station = await self._async_do_request(
            f"{BASE_URL}/stations/{uuid}.json",
            {
                "prettyprint": "false",
                "includeTimeseries": "true",
                "includeCurrentMeasurement": "true",
            },
        )

        return StationMeasurements(station["timeseries"])
