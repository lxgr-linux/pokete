import json
import logging
import os
from pathlib import Path

from pokete import release
from pokete.base.input import hotkeys_save
from . import timer
from .achievements import achievements
from .multiplayer.connector import com_service
from .multiplayer.modeprovider import modeProvider, Mode
from .pokete_care import pokete_care
from .settings import settings

HOME = Path.home()


def save(figure):
    _map = figure.map.name
    old_map = figure.oldmap.name
    x = figure.x
    y = figure.y
    last_center_map = figure.last_center_map.name
    if modeProvider.mode == Mode.MULTI:
        _map, old_map, last_center_map, x, y = com_service.saved_pos

    """Saves all relevant data to savefile"""
    _si = {
        "user": figure.name,
        "represent_char": figure.char,
        "ver": release.VERSION,
        "map": _map,
        "oldmap": old_map,
        "last_center_map": last_center_map,
        "x": x,
        "y": y,
        "achievements": achievements.achieved,
        "pokes": {i: poke.dict() for i, poke in enumerate(figure.pokes)},
        "inv": figure.get_inv(),
        "money": figure.get_money(),
        "settings": settings.to_dict(),
        "caught_poketes": list(dict.fromkeys(figure.caught_pokes
                                             + [i.identifier
                                                for i in figure.pokes])),
        "visited_maps": figure.visited_maps,
        "hotkeys": hotkeys_save(),
        # filters doublicates from figure.used_npcs
        "used_npcs": list(dict.fromkeys(figure.used_npcs)),
        "pokete_care": pokete_care.dict(),
        "time": timer.time.time,
    }
    with open(release.SAVEPATH / "pokete.json", "w+") as file:
        # writes the data to the save file in a nice format
        json.dump(_si, file, indent=4)
    logging.info("[General] Saved")


def read_save():
    """Reads from savefile
    RETURNS:
        session_info dict"""
    Path(release.SAVEPATH).mkdir(parents=True, exist_ok=True)
    # Default test session_info
    _si = {
        "user": "DEFAULT",
        "represent_char": "a",
        "ver": release.VERSION,
        "map": "intromap",
        "oldmap": "playmap_1",
        "last_center_map": "playmap_1",
        "x": 4,
        "y": 5,
        "achievements": [],
        "pokes": {
            "0": {"name": "steini", "xp": 50, "hp": "SKIP",
                  "ap": ["SKIP", "SKIP"]}
        },
        "inv": {"poketeball": 15, "healing_potion": 1},
        "settings": {
            "load_mods": False},
        "figure.caught_pokes": ["steini"],
        "visited_maps": ["playmap_1"],
        "used_npcs": [],
        "hotkeys": {},
        "pokete_care": {
            "entry": 0,
            "poke": None,
        },
        "time": 0
    }

    save_file = release.SAVEPATH / "pokete.json"
    old_save_file = HOME / ".cache" / "pokete" / "pokete.json"
    ancient_save_file = HOME / ".cache" / "pokete" / "pokete.py"

    if os.path.exists(save_file):
        with open(save_file) as _file:
            _si = json.load(_file)
    elif os.path.exists(old_save_file):
        with open(old_save_file) as _file:
            _si = json.load(_file)
    elif os.path.exists(ancient_save_file):
        l_dict = {}
        with open(ancient_save_file, "r") as _file:
            exec(_file.read(), {"session_info": _si}, l_dict)
        _si = json.loads(json.dumps(l_dict["session_info"]))
    return _si
