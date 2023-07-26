[![Test](https://github.com/mib1185/aiopegelonline/actions/workflows/test.yml/badge.svg)](https://github.com/mib1185/aiopegelonline/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/mib1185/aiopegelonline/branch/main/graph/badge.svg?token=QRC1NSIONL)](https://codecov.io/gh/mib1185/aiopegelonline)
[![Library version](https://img.shields.io/pypi/v/aiopegelonline.svg)](https://pypi.org/project/aiopegelonline)
[![Supported versions](https://img.shields.io/pypi/pyversions/aiopegelonline.svg)](https://pypi.org/project/aiopegelonline)
[![Downloads](https://pepy.tech/badge/aiopegelonline)](https://pypi.org/project/aiopegelonline)
[![Formated with Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# aiopegelonline

Asynchronous library to retrieve data from [PEGELONLINE](https://www.pegelonline.wsv.de/).

:warning: **this is in early development state** :warning:

breaking changes may occure at every time

## Requirements

- Python >= 3.9
- aiohttp

## Installation

```bash
pip install aiopegelonline
```

## Examples
### Get all available measurement stations

```python
import asyncio
import aiohttp
from aiopegelonline import PegelOnline


async def main():
    async with aiohttp.ClientSession() as session:
        pegelonline = PegelOnline(session)
        stations = await pegelonline.async_get_all_stations()
        for uuid, station in stations.items():
            print(f"uuid: {uuid} name: {station.name}")


if __name__ == "__main__":
    asyncio.run(main())
```

### Get current measurement

```python
import asyncio
import aiohttp
from aiopegelonline import PegelOnline


async def main():
    async with aiohttp.ClientSession() as session:
        pegelonline = PegelOnline(session)
        measurements = await pegelonline.async_get_station_measurements("70272185-b2b3-4178-96b8-43bea330dcae")

    for name, data in measurements.as_dict().items():
        if data is None:
            print(f"{name} not provided by measurement station")
        else:
            print(f"{name}: {data.value} {data.uom}")

if __name__ == "__main__":
    asyncio.run(main())
```

## References

- [PEGELONLINE api reference (German)](https://www.pegelonline.wsv.de/webservice/dokuRestapi)
