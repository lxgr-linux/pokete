"""Contains classes ralated to the mode choosing meni"""

import sys
import threading

import scrap_engine as se

import pokete_classes.game_map as gm
from pokete_classes.hotkeys import get_action, ACTION_DIRECTIONS, Action
from pokete_classes.loops import std_loop
from pokete_classes.multiplayer.modeprovider import modeProvider, Mode
from pokete_classes.tss import tss
from pokete_classes.ui_elements import BetterChooseBox
from . import connector
from .response_manager import ResponseManager


class PreGameMap(gm.GameSubmap):
    """Map for background"""

    def resize_view(self):
        """Manages recursive view resizing"""
        self.resize(tss.height - 1, tss.width, " ")
        self.remap()


class ModeChooser(BetterChooseBox):
    """The menu to choose modes in"""

    def __init__(self):
        self.map = PreGameMap(
            se.Map(0, 0, " "),
            0, 0,
            tss.height - 1, tss.width,
            "PreGameMap"
        )
        super().__init__(
            1, [
                se.Text("Singleplayer", state="float"),
                se.Text("Multiplayer", state="float"),
                se.Text("Leave...", state="float"),
            ], name="Mode",
            overview=self.map,
            _map=self.map
        )

    def __call__(self):
        """Opens the menu"""
        with self:
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
                            return
                        elif num == 1:
                            connector.connector(self.map, self)
                            modeProvider.mode = Mode.MULTI
                            threading.Thread(
                                target=ResponseManager(),
                                daemon=True
                            ).start()
                            return
                        else:
                            sys.exit()
                std_loop(box=self)
                self.map.show()
