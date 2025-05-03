import sys

import scrap_engine as se

from pokete import data
from pokete.base.context import Context
from pokete.base.exception_propagation import (
    exception_propagating_periodic_event,
)
from pokete.base.game_map import GameSubmap
from pokete.base.input import hotkeys_from_save
from pokete.base.input_loops import ask_bool
from pokete.base.periodic_event_manager import (
    PeriodicEvent,
    PeriodicEventManager,
)
from pokete.base.tss import tss
from pokete.base.ui import Overview
from pokete.classes import ob_maps as obmp
from pokete.classes.asset_service.resources.maps import Map
from pokete.classes.asset_service.resources.obmaps import Obmap
from pokete.classes.audio import audio
from pokete.classes.classes import PlayMap
from pokete.classes.generate import gen_single_map, gen_single_map_obs
from pokete.classes.map_additions.center import CenterMap, ShopMap
from pokete.classes.multiplayer.menu import ModeChooser
from pokete.release import VERSION
from pokete.util import liner
from pokete.util.semantic_version import SemanticVersion


class BGMoverEvent(PeriodicEvent):
    def __init__(self, _map: se.Submap):
        self.map = _map
        self.up = True
        self.right = True

    def tick(self, tick: int):
        if tick % 2 == 0:
            if self.map.x + self.map.width >= self.map.bmap.width:
                self.right = False
            elif self.map.x == 0:
                self.right = True
            if self.map.y + self.map.height >= self.map.bmap.height:
                self.up = False
            elif self.map.y == 0:
                self.up = True
            self.map.set(
                self.map.x + (1 if self.right else -1),
                self.map.y + (1 if self.up else -1),
            )


class PreGameMap(GameSubmap, Overview):
    """Map for background"""

    def __init__(self):
        super().__init__(
            self.build_bg_map(),
            0,
            0,
            tss.height - 1,
            tss.width,
            "PreGameMap",
        )

    @staticmethod
    def build_bg_map() -> PlayMap:
        # Stupidly big setup
        map_key = "playmap_39"
        obmp.ob_maps["centermap"] = CenterMap(50, 50)
        obmp.ob_maps["shopmap"] = ShopMap(50, 50)

        bg_map = Map.from_dict(data.maps[map_key])
        bg_obmap = Obmap.from_dict(data.map_data[map_key])
        assert bg_map is not None
        assert bg_obmap is not None

        bg_playmap = gen_single_map("pregame", bg_map)
        gen_single_map_obs(bg_playmap, bg_obmap, [])

        return bg_playmap

    def resize_view(self):
        """Manages recursive view resizing"""
        self.resize(tss.height - 1, tss.width, " ")
        self.remap()

    def __call__(self, session_info, figure):
        pevm = PeriodicEventManager(
            [exception_propagating_periodic_event, BGMoverEvent(self)]
        )
        ctx = Context(pevm, self, self, figure)
        audio.switch("xDeviruchi - Minigame .mp3")
        hotkeys_from_save(
            ctx,
            session_info.get("hotkeys", {}),
            check_version(ctx, session_info),
        )
        ModeChooser()(ctx)


def check_version(ctx: Context, sinfo):
    """Checks if version in save file is the same as current version
    ARGS:
        sinfo: session_info dict"""
    if "ver" not in sinfo:
        return False
    ver = sinfo["ver"]
    if SemanticVersion.parse(VERSION) < SemanticVersion.parse(ver):
        if not ask_bool(
            ctx,
            liner(
                f"The save file was created \
on version '{ver}', the current version is '{VERSION}', \
such a downgrade may result in data loss! \
Do you want to continue?",
                int(tss.width * 2 / 3),
            ),
        ):
            sys.exit()
    return VERSION != ver
