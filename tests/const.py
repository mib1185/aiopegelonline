"""Constants for aiopegelonline tests."""

from aiohttp import ClientError

MOCK_STATION_DATA_DRESDEN = {
    "uuid": "70272185-xxxx-xxxx-xxxx-43bea330dcae",
    "number": "501060",
    "shortname": "DRESDEN",
    "longname": "DRESDEN",
    "km": 55.63,
    "agency": "STANDORT DRESDEN",
    "longitude": 13.738831783620384,
    "latitude": 51.054459765598125,
    "water": {"shortname": "ELBE", "longname": "ELBE"},
}

MOCK_MEASUREMENT_DATA_HANAU_BRIDGE = {
    "uuid": "07374faf-xxxx-xxxx-xxxx-adc0e0784c4b",
    "number": "24700347",
    "shortname": "HANAU BRÜCKE DFH",
    "longname": "HANAU BRÜCKE DFH",
    "km": 56.398,
    "agency": "ASCHAFFENBURG",
    "water": {"shortname": "MAIN", "longname": "MAIN"},
    "timeseries": [
        {
            "shortname": "DFH",
            "longname": "DURCHFAHRTSHÖHE",
            "unit": "cm",
            "equidistance": 15,
            "currentMeasurement": {
                "timestamp": "2023-07-26T19:45:00+02:00",
                "value": 715,
            },
            "gaugeZero": {
                "unit": "m. ü. NHN",
                "value": 106.501,
                "validFrom": "2019-11-01",
            },
        }
    ],
}

MOCK_STATION_DATA_WUERZBURG = {
    "uuid": "915d76e1-xxxx-xxxx-xxxx-4d144cd771cc",
    "number": "24300600",
    "shortname": "WÜRZBURG",
    "longname": "WÜRZBURG",
    "km": 251.97,
    "agency": "SCHWEINFURT",
    "longitude": 9.925968763247354,
    "latitude": 49.79620901036012,
    "water": {"shortname": "MAIN", "longname": "MAIN"},
}

MOCK_MEASUREMENT_DATA_WUERZBURG = {
    **MOCK_STATION_DATA_WUERZBURG,
    "timeseries": [
        {
            "shortname": "W",
            "longname": "WASSERSTAND ROHDATEN",
            "unit": "cm",
            "equidistance": 15,
            "currentMeasurement": {
                "timestamp": "2023-07-26T19:15:00+02:00",
                "value": 159,
                "stateMnwMhw": "normal",
                "stateNswHsw": "normal",
            },
            "gaugeZero": {
                "unit": "m. ü. NHN",
                "value": 164.511,
                "validFrom": "2019-11-01",
            },
        },
        {
            "shortname": "LT",
            "longname": "LUFTTEMPERATUR",
            "unit": "°C",
            "equidistance": 60,
            "currentMeasurement": {
                "timestamp": "2023-07-26T19:00:00+02:00",
                "value": 21.2,
            },
        },
        {
            "shortname": "WT",
            "longname": "WASSERTEMPERATUR",
            "unit": "°C",
            "equidistance": 60,
            "currentMeasurement": {
                "timestamp": "2023-07-26T19:00:00+02:00",
                "value": 22.1,
            },
        },
        {
            "shortname": "VA",
            "longname": "FLIESSGESCHWINDIGKEIT",
            "unit": "m/s",
            "equidistance": 15,
            "currentMeasurement": {
                "timestamp": "2023-07-26T19:15:00+02:00",
                "value": 0.58,
            },
        },
        {
            "shortname": "O2",
            "longname": "SAUERSTOFFGEHALT",
            "unit": "mg/l",
            "equidistance": 60,
            "currentMeasurement": {
                "timestamp": "2023-07-26T19:00:00+02:00",
                "value": 8.4,
            },
        },
        {
            "shortname": "PH",
            "longname": "PH-WERT",
            "unit": "--",
            "equidistance": 60,
            "currentMeasurement": {
                "timestamp": "2023-07-26T19:00:00+02:00",
                "value": 8.1,
            },
        },
        {
            "shortname": "Q",
            "longname": "ABFLUSS",
            "unit": "m³/s",
            "equidistance": 15,
            "currentMeasurement": {
                "timestamp": "2023-07-26T19:00:00+02:00",
                "value": 102,
            },
        },
    ],
}

MOCK_DATA = {
    "stations.json?prettyprint=false": {
        "status": 200,
        "body": [
            MOCK_STATION_DATA_DRESDEN,
            MOCK_STATION_DATA_WUERZBURG,
        ],
    },
    "stations.json?prettyprint=false&latitude=13&longitude=51&radius=25": {
        "status": 200,
        "body": [
            MOCK_STATION_DATA_DRESDEN,
        ],
    },
    "stations.json?prettyprint=false&latitude=10&longitude=45&radius=25": {
        "status": 200,
        "body": [],
    },
    "stations/70272185-xxxx-xxxx-xxxx-43bea330dcae.json?prettyprint=false": {
        "status": 200,
        "body": MOCK_STATION_DATA_DRESDEN,
    },
    "stations/INVALID_UUID.json?prettyprint=false": {
        "status": 404,
        "body": {
            "status": 404,
            "message": "station not found",
        },
    },
    "stations/CONNECT_ERROR.json?prettyprint=false": {
        "status": None,
        "body": None,
        "exception": ClientError,
    },
    "stations/915d76e1-xxxx-xxxx-xxxx-4d144cd771cc.json?prettyprint=false&includeTimeseries=true&includeCurrentMeasurement=true": {
        "status": 200,
        "body": MOCK_MEASUREMENT_DATA_WUERZBURG,
    },
    "stations/07374faf-xxxx-xxxx-xxxx-adc0e0784c4b.json?prettyprint=false&includeTimeseries=true&includeCurrentMeasurement=true": {
        "status": 200,
        "body": MOCK_MEASUREMENT_DATA_HANAU_BRIDGE,
    },
}
