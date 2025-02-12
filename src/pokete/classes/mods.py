"""This file contains all classes related to mods"""
import logging
import sys

import pokete.data as p_data
from pokete.base.ui.elements import InfoBox
from .side_loops import LoopBox
from .settings import settings


class DummyMods:
    """Dummy Mods class used when mods are disabled"""

    def __init__(self):
        self.mod_info = {}
        self.mod_obs = []
        self.mod_names = []


class ModError(Exception):
    """
    An Error that is thrown, when an inproper module is loaded
    ARGS:
        name: The mod's name
        err: The error that was thrown"""

    def __init__(self, name, err):
        self.name = name
        self.err = err
        super().__init__(f"The mod '{name}' lacks attributes!\n{err}")


class ModInfo(LoopBox):
    """Gives information about mods"""

    def __init__(self):
        self.text = f"""
Mods are { {True: 'enabled', False: 'disabled'}[settings("load_mods").val]}!
To load a mod, it has to be placed in '/mods',
and mods have to be enabled in the menu.

Currently {len(loaded_mods.mod_info)} mod{"s are" if len(loaded_mods.mod_info) != 1 else " is"} loaded:
   """ + "\n   ".join(f"{i}-{loaded_mods.mod_info[i]}" for i in
                      loaded_mods.mod_info) + "\n"
        super().__init__(
            InfoBox(
                self.text, name="Mods",
            )
        )


def try_load_mods(_map):
    global loaded_mods
    if settings("load_mods").val:
        try:
            import mods
        except ModError as mod_err:
            error_box = InfoBox(str(mod_err), "Mod-loading Error")
            error_box.center_add(_map)
            _map.show()
            sys.exit(1)

        for mod in mods.mod_obs:
            mod.mod_p_data(p_data)
    else:
        loaded_mods = DummyMods()
    logging.info("[General] %d mods are loaded: (%s)",
                 len(loaded_mods.mod_obs), ', '.join(loaded_mods.mod_names))


loaded_mods = DummyMods()

if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
