"""This file contains all classes related to mods"""
from .color import Color
from .side_loops import About
from .ui_elements import InfoBox
from .settings import settings
from .language import lang


class DummyMods:
    """Dummy Mods class used when mods are disabled"""

    def __init__(self):
        self.mod_info = {}
        self.mod_obs = []
        self.mod_names = []


class ModError(Exception):
    """
    An Error that is thrown, when an improper module is loaded
    ARGS:
        name: The mod's name
        err: The error that was thrown"""

    def __init__(self, name, err):
        self.name = name
        self.err = err
        super().__init__(lang.str("error.mod.attributes") % (name, err))


class ModInfo(About):
    """Gives information about mods
    ARGS:
        _map: The se.Map the info is shown on
        mod_info: mod_info dict"""

    def __init__(self, _map, mod_info):
        lang_key = f"ui.mods.currently.{'singular' if len(mod_info) == 1 else 'plural'}"
        mod_status = f"ui.mods.{ {True: 'enabled', False: 'disabled'}[settings('load_mods').val]}"

        self.text = f"{lang.str('ui.mods.description') % lang.str(mod_status)}" \
                    f"\n\n{lang.str(lang_key)}" + "\n   ".join(
                    f"{i}-{mod_info[i]}" for i in mod_info) + "\n "
        self.box = InfoBox(self.text, name=lang.str("ui.mods.title"), _map=_map)


if __name__ == "__main__":
    print(f"\033[31;1mDo not execute this!{Color.reset}")
