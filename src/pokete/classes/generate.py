"""Generating maps"""

import math
from typing import Optional

import scrap_engine as se

from pokete.base.periodic_event_manager import PeriodicEvent
from pokete.base.tss import tss
from pokete.classes.asset_service.resources.obmaps import Obmap
from pokete.classes.map_additions import customizers

from . import ob_maps as obmp
from .asset_service.resources import Map
from .asset_service.service import asset_service
from .classes import PlayMap
from .doors import Door, DoorToCenter, DoorToShop
from .landscape import Meadow, Poketeball, Sand, Water
from .map_additions.center import CenterMap, ShopMap
from .npcs import NPC, Trainer
from .poke import Poke
from .settings import settings


class Playmap7Event(PeriodicEvent):
    def __init__(self, fig):
        self.fig = fig
        self.init = False

    def tick(self, tick: int):
        if not self.init:
            self.init = True
            for obj in self.__all_obs():
                obj.bchar = obj.char
                obj.rechar(" ")
        for obj in self.__all_obs():
            if (
                obj.added
                and math.sqrt(
                    (obj.y - self.fig.y) ** 2 + (obj.x - self.fig.x) ** 2
                )
                <= 3
            ):
                obj.rechar(obj.bchar)
            else:
                obj.rechar(" ")

    def __all_obs(self):
        _map = obmp.ob_maps["playmap_7"]
        return (
            _map.get_obj("inner_walls").obs
            + [i.main_ob for i in _map.trainers]
            + [
                obmp.ob_maps["playmap_7"].get_obj(i)
                for i in asset_service.get_assets().obmaps["playmap_7"].balls
                if "playmap_7." + i not in self.fig.used_npcs
                or not settings("save_trainers").val
            ]
        )


def __parse_obj(_map, name, obj, _dict):
    """Parses an object to a maps attribute and adds it
    ARGS:
        _map: The given PlayMap
        name: Name of the attribute
        obj: Object beeing set
        _dict: Dict containing info"""
    _map.register_obj(name, obj)
    obj.add(_map, _dict.x, _dict.y)


def gen_single_map(
    ob_map: str,
    args: Map,
    extra_actions: Optional[dict[str, list[PeriodicEvent]]] = None,
) -> PlayMap:
    playmap = PlayMap(
        name=ob_map,
        height=args.height,
        width=args.width,
        poke_args=args.poke_args,
        w_poke_args=args.w_poke_args,
        weather=args.weather,
        song=args.song,
        pretty_name=args.pretty_name,
        extra_actions=(
            extra_actions.get(args.extra_actions)
            if args.extra_actions is not None and extra_actions is not None
            else None
        ),
    )
    if ob_map in customizers:
        customizers[ob_map].customize(playmap)

    return playmap


def gen_single_map_obs(_map: PlayMap, single_map: Obmap, used_npcs: list[str]):
    for hard_ob, single_hard_ob in single_map.hard_obs.items():
        __parse_obj(
            _map,
            hard_ob,
            se.Text(single_hard_ob.txt, ignore=" "),
            single_hard_ob,
        )
    for soft_ob, single_soft_ob in single_map.soft_obs.items():
        cls = {
            "sand": Sand,
            "meadow": Meadow,
            "water": Water,
        }[single_soft_ob.cls if single_soft_ob.cls is not None else "meadow"]
        __parse_obj(
            _map,
            soft_ob,
            cls(
                single_soft_ob.txt,
                _map.poke_args if cls != Water else _map.w_poke_args,
            ),
            single_soft_ob,
        )
    for door, single_door in single_map.dors.items():
        __parse_obj(
            _map,
            door,
            Door(" ", state="float", arg_proto=single_door.args.to_dict()),
            single_door,
        )
    for ball, single_ball in single_map.balls.items():
        if (
            f"{_map.name}.{ball}" not in used_npcs
            or not settings("save_trainers").val
        ):
            __parse_obj(
                _map, ball, Poketeball(f"{_map.name}.{ball}"), single_ball
            )
    if single_map.special_dors is not None:
        for name, cls in [("dor", DoorToCenter), ("shopdor", DoorToShop)]:
            door_ob = getattr(single_map.special_dors, name)
            if door_ob is not None:
                obj = cls()
                setattr(_map, name, obj)
                obj.add(_map, door_ob.x, door_ob.y)


def gen_maps(
    p_maps: dict[str, Map],
    extra_actions: Optional[dict[str, list[PeriodicEvent]]] = None,
    fix_center=False,
) -> dict[str, PlayMap]:
    """Generates all maps
    ARGS:
        p_maps: contains maps data
        extra_actions: contains ExtraActions class
        fix_center: Whether or not the pokete center should have a fixed size
    RETURNS:
        Dict of all PlayMaps"""
    maps = {}
    for ob_map, args in p_maps.items():
        maps[ob_map] = gen_single_map(ob_map, args, extra_actions)

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


def gen_obs(figure):
    """Generates all objects on the maps
    ARSG:
        map_data: Contains map_data
        npcs: Contains npc data
        trainers: Contains trainers data
        figure: Figure instance"""

    assets = asset_service.get_assets()

    extra_actions: dict[str, list[PeriodicEvent]] = {
        "playmap_7": [Playmap7Event(figure)]
    }

    obmp.ob_maps = gen_maps(assets.maps, extra_actions, True)

    # adding all trainer to map
    for i, map_trainers in assets.trainers.items():
        _map = obmp.ob_maps[i]
        for j in map_trainers.trainers:
            args = j.args
            trainer = Trainer(
                [Poke.wild(p.name, p.xp) for p in j.pokes],
                args.name,
                args.gender,
                args.texts,
                args.lose_texts,
                args.win_texts,
            )
            trainer.add(_map, args.x, args.y)
            _map.trainers.append(trainer)

    # generating objects from map_data
    for ob_map, single_map in assets.obmaps.items():
        gen_single_map_obs(obmp.ob_maps[ob_map], single_map, figure.used_npcs)

    # NPCs
    for npc, _npc in assets.npcs.items():
        NPC(npc, _npc.texts, _fn=_npc.fn, chat=_npc.chat).add(
            obmp.ob_maps[_npc.map], _npc.x, _npc.y
        )


if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
