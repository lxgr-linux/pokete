import os
import importlib

mod_names = [i.strip(".py") for i in os.listdir(__file__.strip("__init__.py"))
             if i[0] != "_"]

mod_obs = [importlib.import_module("mods."+i) for i in mod_names]

mod_info = {i.name : i.version for i in mod_obs}
