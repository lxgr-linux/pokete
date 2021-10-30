import os
import importlib


class ModError(Exception):
    """
    An Error that is thrown, when an inproper module is loaded.
    """

    def __init__(self, name):
        self.name = name
        super().__init__(f"The mod '{name}' lacks attributes!")


mod_names = [i.strip(".py") for i in os.listdir(__file__.strip("__init__.py"))
             if i[0] != "_"]

mod_obs = [importlib.import_module("mods."+i) for i in mod_names]

for name, mod in zip(mod_names, mod_obs):
    try:
       [mod.version, mod.name, mod.mod_p_data]
    except AttributeError:
        raise ModError(name)

mod_info = {i.name : i.version for i in mod_obs}
