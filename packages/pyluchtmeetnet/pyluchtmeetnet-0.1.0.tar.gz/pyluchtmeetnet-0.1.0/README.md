# pyluchtmeetnet

A python package to use the [Luchtmeetnet 2020 OpenAPI][luchtmeetnet-api].

## Installation

```shell
$ pip3 install pyluchtmeetnet
```

## Code example

```python
from pymluchtmeetnet import Luchtmeetnet

latitude = 51.7
longitude = 4.5

# Get nearest station
station = Luchtmeetnet().get_nearest_station(latitude, longitude)
print(station)

# Get latest LKI from station
lki = Luchtmeetnet().get_latest_station_lki(station["number"])
print(lki)

# Get latest measurements from station
measurements = Luchtmeetnet().get_latest_station_measurements(station["number"])
print(measurements)
```

[luchtmeetnet-api]: https://api-docs.luchtmeetnet.nl/
