"""Pegelonline library."""

from __future__ import annotations

import json

from aiohttp.client import ClientSession

from .const import BASE_URL, CONNECT_ERRORS, LOGGER
from .exceptions import PegelonlineDataError
from .models import CacheEntry, Station, StationMeasurements


class PegelOnline:
    """Pegelonline api."""

    def __init__(self, aiohttp_session: ClientSession) -> None:
        """Pegelonline api init."""
        self.session: ClientSession = aiohttp_session
        self.cache: dict[str, CacheEntry] = {}

    async def _async_do_request(self, url: str, params: dict):
        """Perform an async request."""
        cache_key = f"{url}_{params}"
        if cache_key not in self.cache:
            self.cache[cache_key] = CacheEntry(None, None)

        cache_entry = self.cache[cache_key]

        headers = {}
        if (etag := cache_entry.etag) is not None:
            headers = {"If-None-Match": etag}

        LOGGER.debug("REQUEST url: %s params: %s headers: %s", url, params, headers)
        try:
            async with self.session.get(url, params=params, headers=headers) as resp:
                result = await resp.text()
                LOGGER.debug("RESPONSE status: %s text: %s", resp.status, result)

                if resp.status == 304:  # 304 = not modified
                    return cache_entry.result

                if cache_entry.etag is None:
                    cache_entry.etag = resp.headers.get("Etag")

                result = json.loads(result)
                cache_entry.result = result
                if resp.status != 200:
                    raise PegelonlineDataError(
                        result.get("status"), result.get("message")
                    )
        except CONNECT_ERRORS as err:
            LOGGER.debug("connection error", exc_info=True)
            LOGGER.error(
                "Error while getting data: %s: %s",
                err.__class__.__name__,
                err.__class__.__cause__,
            )
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

        LOGGER.debug("all stations: %s", result)

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

        LOGGER.debug("nearby stations: %s", result)

        return result

    async def async_get_station_details(self, uuid: str) -> Station:
        """Get station details."""
        station = await self._async_do_request(
            f"{BASE_URL}/stations/{uuid}.json", {"prettyprint": "false"}
        )

        result = Station(station)

        LOGGER.debug("station %s details: %s", uuid, result)

        return result

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

        result = StationMeasurements(station["timeseries"])

        LOGGER.debug("station %s measurements: %s", uuid, result)

        return result
