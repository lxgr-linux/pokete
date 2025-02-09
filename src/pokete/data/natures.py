"""Contains data about the different natures"""
from pokete.classes.asset_service.resources.base import NatureDict

natures: dict[str, NatureDict] = {
    "brave": {
        "esc": "blue",
        "atc": 1.1,
        "def_": 0.9
    },
    "relaxed": {
        "esc": "green",
        "atc": 0.9,
        "def_": 1.1,
    },
    "hasty": {
        "esc": "red",
        "def_": 0.9,
        "init": 1.1
    },
    "normal": {}
}
