"""Contains classes ralated to the mode choosing meni"""

import sys
import scrap_engine as se

from pokete.base import loops
from pokete.base.context import Context
from pokete.base.input import get_action, ACTION_DIRECTIONS, Action
from pokete.base.input_loops import ask_ok
from pokete.base.ui.elements import BetterChooseBox
from .interactions import movemap_deco
from .pc_manager import pc_manager
from .. import roadmap
from ..asset_service.service import asset_service, ValidationException
from ..generate import gen_obs
from ..landscape import MapInteract
from ..npcs.data import base_npc_actions, npc_actions
from ..multiplayer.modeprovider import modeProvider, Mode
from ..npcs import NPC
from ..pokete_care import PoketeCareNPCAction, pokete_care
from . import connector
from .communication import com_service


class ModeChooser(BetterChooseBox):
    """The menu to choose modes in"""

    def __init__(self):
        super().__init__(
            1, [
                se.Text("Singleplayer", state="float"),
                se.Text("Multiplayer", state="float"),
                se.Text("Leave...", state="float"),
            ], name="Mode"
        )

    def __choose(self, ctx: Context):
        try:
            while True:
                action = get_action()
                if action.triggers(*ACTION_DIRECTIONS):
                    self.input(action)
                else:
                    if action.triggers(Action.CANCEL):
                        sys.exit()
                    elif action.triggers(Action.ACCEPT):
                        num = self.index[0]
                        if num == 0:
                            modeProvider.mode = Mode.SINGLE
                            movemap_deco.set_blank()
                            asset_service.load_assets_from_p_data()
                            NPC.set_vars({
                                **base_npc_actions, **npc_actions,
                                "playmap_50_npc_29": PoketeCareNPCAction(
                                    pokete_care),
                            })
                        elif num == 1:
                            connector.connector(ctx.with_overview(self))
                            modeProvider.mode = Mode.MULTI
                            movemap_deco.set_inactive()
                            com_service()
                        else:
                            sys.exit()
                        # roadmap.RoadMap.check_maps()
                        gen_obs(ctx.figure)
                        ctx.figure.self_add()
                        MapInteract.set_ctx(ctx)
                        pc_manager.set_waiting_users()
                        roadmap.roadmap = roadmap.RoadMap()
                        return
                loops.std(ctx.with_overview(self))
        except ValidationException as e:
            ask_ok(ctx.with_overview(self),
                   f"An error ocured validating game data:\n{e}")
            self.__choose(ctx)

    def __call__(self, ctx: Context):
        """Opens the menu"""
        self.set_ctx(ctx)
        with self:
            self.__choose(ctx)
