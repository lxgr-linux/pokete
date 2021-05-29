#!/usr/bin/env python3
# This script generates the Pokete wiki
from pokete_data.poketes import *
from pokete_data.attacks import *
from pokete_data.types import *

md_str = """
# Pokete wiki

## Table of contents
1. [Poketes](#poketes)
"""

# Table of contents
for j, poke in enumerate(sorted([i for i in pokes][1:])):
    md_str += f"""   {j+1}. [{pokes[poke]["name"]}](#{poke})\n"""

md_str += "2. [Attacks](#attacks)\n"

for j, atc in enumerate(sorted(attacs)):
    md_str += f"""   {j+1}. [{attacs[atc]["name"]}](#{atc.replace("_", "-")})\n"""

# Poketes
md_str += "3. [Types](#types)\n\n## Poketes"

for poke in sorted([i for i in pokes][1:]):
    evolve_txt = f"""- Evolves to {pokes[pokes[poke]["evolve_poke"]]["name"]} at level {pokes[poke]["evolve_lvl"]}""" if pokes[poke]["evolve_poke"] != "" else "- Does not evolve"
    md_attacks = ""
    for atc in pokes[poke]["attacs"]:
        md_attacks += f"""   + [{attacs[atc]["name"]}](#{atc.replace("_", "-")})\n"""

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
- Attacks:
{md_attacks}
{evolve_txt}
"""

# Attacks
md_str += """
## Attacks

"""

for atc in sorted(attacs):
    md_str += f"""
### {attacs[atc]["name"]}
{attacs[atc]["desc"]}
- Type: [{attacs[atc]["type"].capitalize()}](#types)
- Attack factor: {attacs[atc]["factor"]}
- Missing chance: {attacs[atc]["miss_chance"]}
- Attack points: {attacs[atc]["ap"]}
"""

# Types
md_str += """
## Types

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


# writing to file
with open("wiki.md", "w+") as file:
    file.write(md_str)
