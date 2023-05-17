"""Generating maps"""
import logging

import scrap_engine as se

from pokete_classes.map_additions.center import CenterMap, ShopMap
from pokete_classes.tss import tss
from .landscape import Meadow, Water, Sand, Poketeball
from .classes import PlayMap
from .npcs import Trainer
from .poke import Poke
from .doors import Door, DoorToShop, DoorToCenter
from .npcs import NPC
from .settings import settings
from . import ob_maps as obmp


def parse_obj(_map, name, obj, _dict):
    """Parses an object to a maps attribute and adds it
    ARGS:
        _map: The given PlayMap
        name: Name of the attribute
        obj: Object beeing set
        _dict: Dict containing info"""
    _map.register_obj(name, obj)
    obj.add(_map, _dict["x"], _dict["y"])


def gen_maps(p_maps, extra_actions=None, fix_center=False):
    """Generates all maps
    ARGS:
        p_maps: contains maps data
        extra_actions: contains ExtraActions class
        fix_center: Whether or not the pokete center should have a fixed size
    RETURNS:
        Dict of all PlayMaps"""
    maps = {}
    for ob_map, args in p_maps.items():
        args["extra_actions"] = (getattr(extra_actions, args["extra_actions"],
                                         None)
                                 if args["extra_actions"] is not None
                                 else None and extra_actions)
        maps[ob_map] = PlayMap(name=ob_map, **args)

    _h = tss.height - 1
    _w = tss.width
    if fix_center:
        _h = 50
        _w = 50
    centermap = CenterMap(_h, _w)
    shopmap = ShopMap(_h, _w)
    maps["centermap"] = centermap
    maps["shopmap"] = shopmap
    return maps


def gen_obs(map_data, npcs, trainers, figure):
    """Generates all objects on the maps
    ARSG:
        map_data: Contains map_data
        npcs: Contains npc data
        trainers: Contains trainers data
        figure: Figure instance"""

    # adding all trainer to map
    for i, trainer_list in trainers.items():
        _map = obmp.ob_maps[i]
        for j in trainer_list:
            args = j["args"]
            trainer = Trainer(
                [Poke.wild(p["name"], p["xp"]) for p in j["pokes"]],
                args["name"],
                args["gender"], args["texts"], args["lose_texts"],
                args["win_texts"]
            )
            trainer.add(_map, args["x"], args["y"])
            _map.trainers.append(trainer)

    # generating objects from map_data
    for ob_map, single_map in map_data.items():
        _map = obmp.ob_maps[ob_map]
        for hard_ob, single_hard_ob in single_map["hard_obs"].items():
            parse_obj(_map, hard_ob,
                      se.Text(single_hard_ob["txt"],
                              ignore=" "),
                      single_hard_ob)
        for soft_ob, single_soft_ob in single_map["soft_obs"].items():
            cls = {
                "sand": Sand,
                "meadow": Meadow,
                "water": Water,
            }[single_soft_ob.get("cls", "meadow")]
            parse_obj(_map, soft_ob,
                      cls(single_soft_ob["txt"],
                          _map.poke_args
                          if cls != Water else _map.w_poke_args),
                      single_soft_ob)
        for door, single_door in single_map["dors"].items():
            parse_obj(_map, door,
                      Door(" ", state="float",
                           arg_proto=single_door["args"]),
                      single_door)
        for ball, single_ball in single_map["balls"].items():
            if f'{ob_map}.{ball}' not in figure.used_npcs or not \
                settings("save_trainers").val:
                parse_obj(_map, ball,
                          Poketeball(f"{ob_map}.{ball}"),
                          single_ball)
        if "special_dors" in single_map:
            for name, cls in [("dor", DoorToCenter), ("shopdor", DoorToShop)]:
                if name in single_map["special_dors"]:
                    obj = cls()
                    setattr(_map, name, obj)
                    obj.add(_map, single_map["special_dors"][name]["x"],
                            single_map["special_dors"][name]["y"])

    # NPCs
    for npc, _npc in npcs.items():
        NPC(npc, _npc["texts"], _fn=_npc["fn"],
            chat=_npc.get("chat", None)).add(obmp.ob_maps[_npc["map"]],
                                             _npc["x"], _npc["y"])


if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
