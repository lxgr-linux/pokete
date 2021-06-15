#!/usr/bin/env python3
# This script generates the Pokete wiki
from pokete_data.poketes import *
from pokete_data.attacks import *
from pokete_data.types import *
from pokete_data.items import *
import os

md_str = """# Pokete wiki
This wiki/documentation is a compilation of all Poketes/attacks/types present in the Pokete game.
This wiki can be generated using ```$ gen-wiki.py```.

## Table of contents
1. [Poketes](#poketes)
"""


# Table of contents
for j, poke in enumerate(sorted([i for i in pokes][1:])):
    md_str += f"""   {j+1}. [{pokes[poke]["name"]}](#{poke})\n"""

md_str += "2. [Attacks](#attacks)\n"

for j, atc in enumerate(sorted(attacs)):
    md_str += f"""   {j+1}. [{attacs[atc]["name"]}](#{atc.replace("_", "-")})\n"""

md_str += """3. [Types](#types)
4. [Items](#items)
"""

for j, item in enumerate(sorted(items)):
    md_str += f"""   {j+1}. [{items[item]["pretty_name"]}](#{item.replace("_", "-")})\n"""


# Poketes
md_str += """
## Poketes
In the following all Poketes with their attributes are displayed.
"""

for poke in sorted([i for i in pokes][1:]):
    evolve_txt = f"""- Evolves to {pokes[pokes[poke]["evolve_poke"]]["name"]} at level {pokes[poke]["evolve_lvl"]}""" if pokes[poke]["evolve_poke"] != "" else "- Does not evolve"
    md_attacks = ""
    for atc in pokes[poke]["attacs"]:
        md_attacks += f"""\n   + [{attacs[atc]["name"]}](#{atc.replace("_", "-")})"""

    md_str += f"""
### {pokes[poke]["name"]}
{pokes[poke]["desc"]}
```
{pokes[poke]["ico"]}
```

- Type: [{pokes[poke]["type"].capitalize()}](#types)
- Health points: {pokes[poke]["hp"]}
- Attack factor: {pokes[poke]["atc"].replace("self.lvl()", "level")}
- Defense factor: {pokes[poke]["defense"].replace("self.lvl()", "level")}
- Missing chance: {pokes[poke]["miss_chance"]}
- Rarity: {pokes[poke]["rarity"]}
- Loosing experience: {pokes[poke]["lose_xp"]}
- Attacks:{md_attacks}
{evolve_txt}
"""


# Attacks
md_str += """
## Attacks
Those are all attacks present in the game.
"""

for atc in sorted(attacs):
    md_str += f"""
### {attacs[atc]["name"]}
{attacs[atc]["desc"]}
- Type: [{attacs[atc]["type"].capitalize()}](#types)
- Minimum Level: {attacs[atc]["min_lvl"]}
- Attack factor: {attacs[atc]["factor"]}
- Missing chance: {attacs[atc]["miss_chance"]}
- Attack points: {attacs[atc]["ap"]}
"""


# Types
md_str += """
## Types
Those are all the Pokete/Attack types that are present in the game with all their (in)effectivities against other types.

Type|Effective against|Ineffective against
---|---|---
"""

for type in types:
    effective = ""
    for i in types[type]["effective"]:
        effective += i.capitalize()+(", " if i != types[type]["effective"][-1] else "")
    ineffective = ""
    for i in types[type]["ineffective"]:
        ineffective += i.capitalize()+(", " if i != types[type]["ineffective"][-1] else "")
    md_str += f"{type.capitalize()}|{effective}|{ineffective}\n"


# Items
md_str += """
## Items
Those are all items present in the game, that can be traded or found.
"""

for item in sorted(items):
    md_str += f"""
### {items[item]["pretty_name"]}
{items[item]["desc"]}
- Price: {items[item]["price"]}
- Can be used in fights: {"Yes" if items[item]["fn"] != None else "No"}
"""

# writing to file
with open("wiki.md", "w+") as file:
    file.write(md_str)


# pics.md
md_str = "# Example pictures\n"
for i in sorted(os.listdir("assets/ss")):
    md_str += f"![{i}](ss/{i})\n\n"

# writing to file
with open("assets/pics.md", "w+") as file:
    file.write(md_str)
