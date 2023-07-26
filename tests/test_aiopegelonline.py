"""Tests for aiopegelonline."""
from __future__ import annotations

import pytest
from aiohttp import ClientError

from aiopegelonline.exceptions import PegelonlineDataError
from aiopegelonline.models import Station, StationMeasurements


@pytest.mark.asyncio
async def test_get_all_stations(mock_pegelonline):
    """Test async_get_all_stations."""
    # with mock_response:
    stations = await mock_pegelonline.async_get_all_stations()
    assert len(stations) == 2

    station = stations["70272185-xxxx-xxxx-xxxx-43bea330dcae"]
    assert isinstance(station, Station)
    assert station.as_dict() == {
        "uuid": "70272185-xxxx-xxxx-xxxx-43bea330dcae",
        "name": "DRESDEN",
        "agency": "STANDORT DRESDEN",
        "river_kilometer": 55.63,
        "longitude": 13.738831783620384,
        "latitude": 51.054459765598125,
        "water_name": "ELBE",
        "base_data_url": "https://www.pegelonline.wsv.de/gast/stammdaten?pegelnr=501060",
    }

    station = stations["915d76e1-xxxx-xxxx-xxxx-4d144cd771cc"]
    assert isinstance(station, Station)
    assert station.uuid == "915d76e1-xxxx-xxxx-xxxx-4d144cd771cc"
    assert station.name == "WÜRZBURG"
    assert station.agency == "SCHWEINFURT"
    assert station.river_kilometer == 251.97
    assert station.longitude == 9.925968763247354
    assert station.latitude == 49.79620901036012
    assert station.water_name == "MAIN"
    assert (
        station.base_data_url
        == "https://www.pegelonline.wsv.de/gast/stammdaten?pegelnr=24300600"
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
async def test_get_station_measurements(mock_pegelonline):
    """Test async_get_station_measurements."""
    measurement = await mock_pegelonline.async_get_station_measurements(
        "915d76e1-xxxx-xxxx-xxxx-4d144cd771cc"
    )
    assert isinstance(measurement, StationMeasurements)
    assert measurement.air_temperature is not None
    assert measurement.air_temperature.uom == "°C"
    assert measurement.air_temperature.value == 21.2
    assert measurement.clearance_height is None
    assert measurement.oxygen_level is not None
    assert measurement.oxygen_level.uom == "mg/l"
    assert measurement.oxygen_level.value == 8.4
    assert measurement.ph_value is not None
    assert measurement.ph_value.uom == "--"
    assert measurement.ph_value.value == 8.1
    assert measurement.water_speed is not None
    assert measurement.water_speed.uom == "m/s"
    assert measurement.water_speed.value == 0.58
    assert measurement.water_flow is not None
    assert measurement.water_flow.uom == "m³/s"
    assert measurement.water_flow.value == 102
    assert measurement.water_level is not None
    assert measurement.water_level.uom == "cm"
    assert measurement.water_level.value == 159
    assert measurement.water_temperature is not None
    assert measurement.water_temperature.uom == "°C"
    assert measurement.water_temperature.value == 22.1

    measurement = await mock_pegelonline.async_get_station_measurements(
        "07374faf-xxxx-xxxx-xxxx-adc0e0784c4b"
    )
    assert isinstance(measurement, StationMeasurements)
    assert measurement.clearance_height is not None
    assert measurement.clearance_height.uom == "cm"
    assert measurement.clearance_height.value == 715
    assert measurement.clearance_height.as_dict() == {
        "uom": "cm",
        "value": 715,
    }
    assert measurement.as_dict() == {
        "air_temperature": None,
        "clearance_height": measurement.clearance_height,
        "oxygen_level": None,
        "ph_value": None,
        "water_speed": None,
        "water_flow": None,
        "water_level": None,
        "water_temperature": None,
    }
