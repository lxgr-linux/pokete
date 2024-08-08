"""Contains data about the different natures"""
from pokete_classes.asset_service.asset_types import Natures

natures: Natures = {
    "brave": {
        "esc": "blue",
        "atc": 1.1,
        "_def": 0.9
    },
    "relaxed": {
        "esc": "green",
        "atc": 0.9,
        "_def": 1.1,
    },
    "hasty": {
        "esc": "red",
        "_def": 0.9,
        "init": 1.1
    },
    "normal": {}
}
