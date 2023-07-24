"""Tests for aiopegelonline."""
from __future__ import annotations

import pytest
from aiohttp import ClientError

from aiopegelonline import CurrentMeasurement, Station
from aiopegelonline.exceptions import PegelonlineDataError


@pytest.mark.asyncio
async def test_get_all_stations(mock_pegelonline):
    """Test async_get_all_stations."""
    # with mock_response:
    stations = await mock_pegelonline.async_get_all_stations()
    assert len(stations) == 2

    station = stations["70272185-xxxx-xxxx-xxxx-43bea330dcae"]
    assert isinstance(station, Station)
    assert station.uuid == "70272185-xxxx-xxxx-xxxx-43bea330dcae"
    assert station.name == "DRESDEN"
    assert station.agency == "STANDORT DRESDEN"
    assert station.river_kilometer == 55.63
    assert station.longitude == 13.738831783620384
    assert station.latitude == 51.054459765598125
    assert station.water_name == "ELBE"
    assert (
        station.base_data_url
        == "https://www.pegelonline.wsv.de/gast/stammdaten?pegelnr=501060"
    )

    station = stations["706e5110-xxxx-xxxx-xxxx-c071fcb492ec"]
    assert isinstance(station, Station)
    assert station.uuid == "706e5110-xxxx-xxxx-xxxx-c071fcb492ec"
    assert station.name == "HAMBURG-HARBURG"
    assert station.agency == "HAMBURG PORT AUTHORITY"
    assert station.river_kilometer == 615
    assert station.longitude == 9.991814826063601
    assert station.latitude == 53.472725901227285
    assert station.water_name == "ELBE"
    assert (
        station.base_data_url
        == "https://www.pegelonline.wsv.de/gast/stammdaten?pegelnr=5952025"
    )


@pytest.mark.asyncio
async def test_get_nearby_stations(mock_pegelonline):
    """Test async_get_nearby_stations."""
    stations = await mock_pegelonline.async_get_nearby_stations(13, 51, 25)
    assert len(stations) == 1

    station = stations["70272185-xxxx-xxxx-xxxx-43bea330dcae"]
    assert isinstance(station, Station)
    assert station.uuid == "70272185-xxxx-xxxx-xxxx-43bea330dcae"
    assert station.name == "DRESDEN"
    assert station.agency == "STANDORT DRESDEN"
    assert station.river_kilometer == 55.63
    assert station.longitude == 13.738831783620384
    assert station.latitude == 51.054459765598125
    assert station.water_name == "ELBE"
    assert (
        station.base_data_url
        == "https://www.pegelonline.wsv.de/gast/stammdaten?pegelnr=501060"
    )


@pytest.mark.asyncio
async def test_get_nearby_stations_no_stations(mock_pegelonline):
    """Test async_get_nearby_stations."""
    stations = await mock_pegelonline.async_get_nearby_stations(10, 45, 25)
    assert len(stations) == 0


@pytest.mark.asyncio
async def test_get_station_details(mock_pegelonline):
    """Test async_get_station_details."""
    station = await mock_pegelonline.async_get_station_details(
        "70272185-xxxx-xxxx-xxxx-43bea330dcae"
    )
    assert isinstance(station, Station)
    assert station.uuid == "70272185-xxxx-xxxx-xxxx-43bea330dcae"
    assert station.name == "DRESDEN"
    assert station.agency == "STANDORT DRESDEN"
    assert station.river_kilometer == 55.63
    assert station.longitude == 13.738831783620384
    assert station.latitude == 51.054459765598125
    assert station.water_name == "ELBE"
    assert (
        station.base_data_url
        == "https://www.pegelonline.wsv.de/gast/stammdaten?pegelnr=501060"
    )


@pytest.mark.asyncio
async def test_get_station_details_invalid(mock_pegelonline):
    """Test async_get_station_details with invalid uuid."""
    with pytest.raises(PegelonlineDataError):
        await mock_pegelonline.async_get_station_details("INVALID_UUID")


@pytest.mark.asyncio
async def test_get_station_details_connection_error(mock_pegelonline):
    """Test async_get_station_details with connection error."""
    with pytest.raises(ClientError):
        await mock_pegelonline.async_get_station_details("CONNECT_ERROR")


@pytest.mark.asyncio
async def test_get_station_measurement(mock_pegelonline):
    """Test async_get_station_measurement."""
    measurement = await mock_pegelonline.async_get_station_measurement(
        "70272185-xxxx-xxxx-xxxx-43bea330dcae"
    )
    assert isinstance(measurement, CurrentMeasurement)
    assert measurement.uom == "cm"
    assert measurement.value == 60
