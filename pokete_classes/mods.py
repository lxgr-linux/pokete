"""This file contains all classes related to mods"""

from .side_loops import LoopBox
from .ui_elements import InfoBox
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
    """Gives information about mods
    ARGS:
        _map: The se.Map the info is shown on
        mod_info: mod_info dict"""

    def __init__(self, _map, mod_info):
        self.text = f"""
Mods are { {True: 'enabled', False: 'disabled'}[settings("load_mods").val] }!
To load a mod, it has to be placed in '/mods',
and mods have to be enabled in the menu.

Currently {len(mod_info)} mod{"s are" if len(mod_info) != 1 else " is"} loaded:
   """ + "\n   ".join(f"{i}-{mod_info[i]}" for i in mod_info) + "\n"
        super().__init__(InfoBox(self.text, name="Mods", _map=_map))


if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
