from .side_loops import About
from .ui_elements import InfoBox


class DummyMods:
    """Dummy Mods class used when mods are disabled"""

    def __init__(self):
        self.mod_info = {}
        self.mod_obs = []
        self.mod_names = []


class ModError(Exception):
    """
    An Error that is thrown, when an inproper module is loaded.
    """

    def __init__(self, name, err):
        self.name = name
        self.err = err
        super().__init__(f"The mod '{name}' lacks attributes!\n{err}")


class ModInfo(About):
    """Gives information about mods"""

    def __init__(self, _map, settings, mod_info):
        self.map = _map
        self.text = f"""
Mods are { {True: 'enabled', False: 'disabled'}[settings.load_mods] }!
To load a mod, it has to be placed in '/mods',
and mods have to be enabled in the menu.

Currently {len(mod_info)} mod{"s are" if len(mod_info) != 1 else " is"} loaded:
   """ + "\n   ".join(f"{i}-{mod_info[i]}" for i in mod_info) + "\n"
        self.box = InfoBox(self.text, _map=self.map)
        self.box.name_label.rechar("Mods")
        self.box.info_label.rechar("q:close")
