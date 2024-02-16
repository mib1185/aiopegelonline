"""aiopegelonline models."""

from __future__ import annotations

from dataclasses import dataclass


class Station:
    """Representation of a station."""

    def __init__(self, data: dict) -> None:
        """Initialize station class."""
        self.uuid: str = data["uuid"]
        self.name: str = data["longname"]
        self.agency: str = data["agency"]
        self.river_kilometer: float | None = data.get("km")
        self.longitude: float | None = data.get("longitude")
        self.latitude: float | None = data.get("latitude")
        self.water_name: str = data["water"]["longname"]
        self.base_data_url: str = (
            f"https://www.pegelonline.wsv.de/gast/stammdaten?pegelnr={data['number']}"
        )

    def as_dict(self) -> dict[str, str | float | None]:
        """Return data das dict."""
        return {
            "uuid": self.uuid,
            "name": self.name,
            "agency": self.agency,
            "river_kilometer": self.river_kilometer,
            "longitude": self.longitude,
            "latitude": self.latitude,
            "water_name": self.water_name,
            "base_data_url": self.base_data_url,
        }


class CurrentMeasurement:
    """Representation of a current measurement."""

    def __init__(self, data: dict) -> None:
        """Initialize current measurment class."""
        self.uom: str = data["unit"]
        self.value: float = data["currentMeasurement"]["value"]

    def as_dict(self) -> dict[str, str | float]:
        """Return data das dict."""
        return {
            "uom": self.uom,
            "value": self.value,
        }


class StationMeasurements:
    """Representation of station measurements."""

    def __init__(self, data: list[dict]) -> None:
        """Initialize station measurments class."""
        self.air_temperature: CurrentMeasurement | None = None
        self.clearance_height: CurrentMeasurement | None = None
        self.oxygen_level: CurrentMeasurement | None = None
        self.ph_value: CurrentMeasurement | None = None
        self.water_speed: CurrentMeasurement | None = None
        self.water_flow: CurrentMeasurement | None = None
        self.water_level: CurrentMeasurement | None = None
        self.water_temperature: CurrentMeasurement | None = None

        for measurement in data:
            if measurement["shortname"] == "DFH":
                self.clearance_height = CurrentMeasurement(measurement)
            elif measurement["shortname"] == "LT":
                self.air_temperature = CurrentMeasurement(measurement)
            elif measurement["shortname"] == "O2":
                self.oxygen_level = CurrentMeasurement(measurement)
            elif measurement["shortname"] == "PH":
                self.ph_value = CurrentMeasurement(measurement)
            elif measurement["shortname"] == "Q":
                self.water_flow = CurrentMeasurement(measurement)
            elif measurement["shortname"] == "VA":
                self.water_speed = CurrentMeasurement(measurement)
            elif measurement["shortname"] == "W":
                self.water_level = CurrentMeasurement(measurement)
            elif measurement["shortname"] == "WT":
                self.water_temperature = CurrentMeasurement(measurement)

    def as_dict(self) -> dict[str, CurrentMeasurement | None]:
        """Return data das dict."""
        return {
            "air_temperature": self.air_temperature,
            "clearance_height": self.clearance_height,
            "oxygen_level": self.oxygen_level,
            "ph_value": self.ph_value,
            "water_speed": self.water_speed,
            "water_flow": self.water_flow,
            "water_level": self.water_level,
            "water_temperature": self.water_temperature,
        }


@dataclass
class CacheEntry:
    """Representation of response cache entry."""

    etag: str | None
    result: dict | None
