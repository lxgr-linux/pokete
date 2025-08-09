"""Contains classes ralated to the mode choosing meni"""

import sys
from typing import Optional

import scrap_engine as se

from pokete.base.context import Context
from pokete.base.input_loops import ask_ok
from pokete.base.ui.views.better_choose_box import BetterChooseBoxView

from .. import roadmap
from ..asset_service.service import ValidationException, asset_service
from ..generate import gen_obs
from ..landscape import MapInteract
from ..multiplayer.modeprovider import Mode, modeProvider
from ..npcs import NPC
from ..npcs.data import base_npc_actions, npc_actions
from ..pokete_care import PoketeCareNPCAction, pokete_care
from . import connector
from .communication import com_service
from .interactions import movemap_deco
from .pc_manager import pc_manager


class ModeChooser(BetterChooseBoxView[bool]):
    """The menu to choose modes in"""

    def __init__(self):
        super().__init__(
            1,
            [
                se.Text("Singleplayer", state="float"),
                se.Text("Multiplayer (Beta)", state="float"),
                se.Text("Leave...", state="float"),
            ],
            name="Mode",
        )

    def choose(self, ctx: Context, idx: int) -> Optional[bool]:
        try:
            if idx == 0:
                modeProvider.mode = Mode.SINGLE
                movemap_deco.set_blank()
                asset_service.load_assets_from_p_data()
                NPC.set_vars(
                    {
                        **base_npc_actions,
                        **npc_actions,
                        "playmap_50_npc_29": PoketeCareNPCAction(pokete_care),
                    }
                )
            elif idx == 1:
                connector.connector(ctx)
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
            return True
        except ValidationException as e:
            ask_ok(
                ctx,
                f"An error ocured validating game data:\n{e}",
            )
            return None
