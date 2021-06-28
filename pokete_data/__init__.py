from pokete_data.poketes import *
from pokete_data.attacks import *
from pokete_data.maps import *
from pokete_data.classes import *
from pokete_data.types import *
from pokete_data.items import *
from pokete_data.npcs import *
from pokete_data.mapstations import *


class ValidationError(Exception):
    def __init__(self, value, name, validator):
        super().__init__(f"Value '{value}' is not in '{name}' ({validator})")


def one_validate(ob, validator, name):
    for value in validators[validator]:
        if value not in ob:
            raise ValidationError(value, name, validator)

def single_validate(dict, validator, name = ""):
    for j in dict:
        one_validate(dict[j], validator, f"{name}.{j}")

def validate():
    for i, j in zip([pokes, types, map_data, stations, items, npcs], validators):
        single_validate(i, j)
    for m in map_data:
        for i in ["hard_ob", "soft_ob", "dor", "ball"]:
            single_validate(map_data[m][i+"s"], i, m)
    for s in stations:
        one_validate(stations[s]["gen"], "gen", s+".gen")
        one_validate(stations[s]["add"], "add", s+"add")

validators = {
    "poke": ["name" ,"hp" ,"atc", "defense", "attacs", "miss_chance", "desc", "lose_xp", "rarity", "type", "evolve_poke", "evolve_lvl", "ico", "initiative"],
    "type": ["effective", "ineffective"],
    "playmap": ["hard_obs", "soft_obs", "dors", "balls"],
    "station": ["gen", "add"],
    "item": ["pretty_name", "desc", "price", "fn"],
    "npc": ["texts", "fn", "args", "map", "x", "y"],
    "hard_ob": ["x", "y", "txt"],
    "soft_ob": ["x", "y", "txt"],
    "dor": ["x", "y", "args"],
    "ball": ["x", "y"],
    "gen": ["width", "height"],
    "add": ["x", "y"],
}


if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
