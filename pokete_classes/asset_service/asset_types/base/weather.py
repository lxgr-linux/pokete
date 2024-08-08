from typing import TypedDict


class Weather(TypedDict):
    info: str
    effected: dict[str, float]


Weathers = dict[str, Weather]
