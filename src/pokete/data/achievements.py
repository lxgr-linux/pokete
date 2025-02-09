"""Contains raw achievement data"""
from pokete.classes.asset_service.resources.base import AchievementDict

achievements: dict[str, AchievementDict] = {
    "first_poke": {
        "title": "First Pokete",
        "desc": "Catch your first Pokete!"
    },
    "first_duel": {
        "title": "First duel",
        "desc": "Fight against your first trainer!"
    },
    "catch_em_all": {
        "title": "Catch em all",
        "desc": "Catch all Poketes and fill your Pokete-Dex!"
    },
    "first_evolve": {
        "title": "First evolution",
        "desc": "Evolve your first Pokete!"
    },
}
