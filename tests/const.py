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

MOCK_MEASUREMENT_DATA_DRESDEN = {
    "shortname": "W",
    "longname": "WASSERSTAND ROHDATEN",
    "unit": "cm",
    "equidistance": 15,
    "currentMeasurement": {
        "timestamp": "2023-07-24T23:00:00+02:00",
        "value": 60,
        "stateMnwMhw": "low",
        "stateNswHsw": "normal",
    },
    "gaugeZero": {"unit": "m. ü. NHN", "value": 102.7, "validFrom": "2019-11-01"},
}

MOCK_STATION_DATA_HAMBURG = {
    "uuid": "706e5110-xxxx-xxxx-xxxx-c071fcb492ec",
    "number": "5952025",
    "shortname": "HAMBURG-HARBURG",
    "longname": "HAMBURG-HARBURG",
    "km": 615,
    "agency": "HAMBURG PORT AUTHORITY",
    "longitude": 9.991814826063601,
    "latitude": 53.472725901227285,
    "water": {"shortname": "ELBE", "longname": "ELBE"},
}

MOCK_DATA = {
    "stations.json?prettyprint=false": {
        "status": 200,
        "body": [
            MOCK_STATION_DATA_DRESDEN,
            MOCK_STATION_DATA_HAMBURG,
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
    "stations/70272185-xxxx-xxxx-xxxx-43bea330dcae/W.json?prettyprint=false&includeCurrentMeasurement=true": {
        "status": 200,
        "body": MOCK_MEASUREMENT_DATA_DRESDEN,
    },
}
