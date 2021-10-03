from pokete_data.poketes import *
from pokete_data.attacks import *
from pokete_data.map_data import *
from pokete_data.types import *
from pokete_data.items import *
from pokete_data.trainers import *
from pokete_data.npcs import *
from pokete_data.mapstations import *
from pokete_data.maps import *


class ValidationError(Exception):
    def __init__(self, value, name, validator):
        super().__init__(f"Value '{value}' is not in '{name}' ({validator})")


def one_validate(ob, validator, name):
    for value in validators[validator]:
        if value not in ob:
            raise ValidationError(value, name, validator)


def single_validate(dict, validator, name=""):
    for j in dict:
        one_validate(dict[j], validator, f"{name}.{j}")


def validate():
    for i, j in zip([pokes, types, map_data, stations, items, npcs, attacks, maps], validators):
        single_validate(i, j)
    for p in pokes:
        for i in pokes[p]["ico"]:
            one_validate(i, "poke_ico", p + ".ico")
    for m in map_data:
        for i in ["hard_ob", "soft_ob", "dor", "ball"]:
            single_validate(map_data[m][i + "s"], i, m)
    for s in stations:
        one_validate(stations[s]["gen"], "gen", s + ".gen")
        one_validate(stations[s]["add"], "add", s + "add")
    for t in trainers:
        for i in trainers[t]:
            one_validate(i, "trainer", t + ".trainer")


validators = {
    "poke": ["name", "hp", "atc", "defense", "attacks", "miss_chance", "desc", "lose_xp", "rarity", "types",
             "evolve_poke", "evolve_lvl", "ico", "initiative"],
    "type": ["effective", "ineffective", "color"],
    "playmap": ["hard_obs", "soft_obs", "dors", "balls"],
    "station": ["gen", "add"],
    "item": ["pretty_name", "desc", "price", "fn"],
    "npc": ["texts", "fn", "args", "map", "x", "y"],
    "attack": ["name", "factor", "action", "move", "miss_chance", "min_lvl", "desc", "type", "effect", "is_generic",
               "ap"],
    "map": ["height", "width", "pretty_name", "extra_actions", "poke_args"],
    "hard_ob": ["x", "y", "txt"],
    "soft_ob": ["x", "y", "txt"],
    "dor": ["x", "y", "args"],
    "ball": ["x", "y"],
    "gen": ["additionals", "width", "height"],
    "add": ["x", "y"],
    "poke_ico": ["txt", "esc"],
    "trainer": ["poke", "args"]
}

if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
