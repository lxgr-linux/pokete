"""This imports all mods and validates them."""

import os
import importlib
from pokete_classes.mods import ModError


mod_names = [i.strip(".py") for i in os.listdir(__file__.strip("__init__.py"))
             if i[0] != "_" and i != "README.md"]

mod_obs = [importlib.import_module("mods."+i) for i in mod_names]

for name, mod in zip(mod_names, mod_obs):
    try:
       [mod.version, mod.name, mod.mod_p_data]
    except AttributeError as err:
        raise ModError(name, err)

mod_info = {i.name : i.version for i in mod_obs}
