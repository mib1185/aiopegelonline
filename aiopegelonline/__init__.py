"""Pegelonline library."""

from __future__ import annotations

from dataclasses import dataclass

from aiohttp.client import ClientSession

from .const import BASE_URL, CONNECT_ERRORS, LOGGER, REQUEST_TIMEOUT
from .exceptions import PegelonlineDataError


@dataclass
class Station:
    """Representation of a station."""

    uuid: str
    name: str
    agency: str
    river_kilometer: float | None
    longitude: float | None
    latitude: float | None
    water_name: str


@dataclass
class CurrentMeasurement:
    """Representation of a current measurement."""

    uom: str
    value: float


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
                result = await resp.json()
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
            result[station["uuid"]] = Station(
                station["uuid"],
                station["longname"],
                station["agency"],
                station.get("km"),
                station.get("longitude"),
                station.get("latitude"),
                station["water"]["longname"],
            )

        return result

    async def async_get_station_measurement(self, uuid: str) -> CurrentMeasurement:
        """Get current measurement of a station."""
        station = await self._async_do_request(
            f"{BASE_URL}/stations/{uuid}.json",
            {
                "prettyprint": "false",
                "includeTimeseries": "true",
                "includeCurrentMeasurement": "true",
                "timeseries": "W",
            },
        )

        measurement = station["timeseries"][0]
        return CurrentMeasurement(
            measurement["unit"], measurement["currentMeasurement"]["value"]
        )
