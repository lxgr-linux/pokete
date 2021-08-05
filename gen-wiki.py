#!/usr/bin/env python3
# This script generates the Pokete wiki
import os
import scrap_engine as se
from pokete_data import *
from pokete_classes.effects import *

def gen_wiki():
    global attacks
    # sorting dicts
    attacks = {i[1]: i[-1] for i in
                    sorted([(attacks[atc]["type"], atc, attacks[atc]) for atc in attacks])}

    with open("Changelog.md", "r") as file:
        ver = file.readline()

    md_str = f"""v{ver}
# Pokete wiki
This wiki/documentation is a compilation of all Poketes/attacks/types present in the Pokete game.
This wiki can be generated using ```$ gen-wiki.py```.

## Table of contents
1. [Poketes](#poketes)
"""

    # Table of contents
    for j, poke in enumerate(sorted(list(pokes)[1:])):
        md_str += f"""   {j+1}. [{pokes[poke]["name"]}](#{poke})\n"""
    md_str += "2. [Attacks](#attacks)\n"
    for j, atc in enumerate(attacks):
        md_str += f"""   {j+1}. [{attacks[atc]["name"]}](#{atc.replace("_", "-")})\n"""
    md_str += """3. [Types](#types)
4. [Items](#items)
"""
    for j, item in enumerate(sorted(items)):
        md_str += f"""   {j+1}. [{items[item]["pretty_name"]}](#{item.replace("_", "-")})\n"""
    md_str += """5. [Effects](#effects)
"""
    for j, effect in enumerate(effects):
        md_str += f"""   {j+1}. [{effect.c_name.capitalize()}](#{effect.c_name.replace("_", "-")})
"""

    # Poketes
    md_str += """
## Poketes
In the following all Poketes with their attributes are displayed.
"""

    for poke in sorted(list(pokes)[1:]):
        evolve_txt = f"""- Evolves to [{pokes[pokes[poke]["evolve_poke"]]["name"]}](#{pokes[poke]["evolve_poke"]}) at level {pokes[poke]["evolve_lvl"]}""" if pokes[poke]["evolve_poke"] != "" else "- Does not evolve"
        md_attacks = ""
        for atc in pokes[poke]["attacks"]:
            md_attacks += f"""\n   + [{attacks[atc]["name"]}](#{atc.replace("_", "-")})"""
        # ico
        ico_map = se.Map(4, 11, background=" ")
        for ico in pokes[poke]["ico"]:
            se.Text(ico["txt"], state="float", ignore=" ").add(ico_map, 0, 0)
        ico = "".join("".join(arr)+"\n" for arr in ico_map.map)
        md_str += f"""
### {pokes[poke]["name"]}
{pokes[poke]["desc"]}

```
{ico}
```

- Type: [{pokes[poke]["type"].capitalize()}](#types)
- Health points: {pokes[poke]["hp"]}
- Attack factor: {pokes[poke]["atc"].replace("self.lvl()", "level")}
- Defense factor: {pokes[poke]["defense"].replace("self.lvl()", "level")}
- Initiative: {pokes[poke]["initiative"].replace("self.lvl()", "level")}
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

    for atc in attacks:
        md_str += f"""
### {attacks[atc]["name"]}
{attacks[atc]["desc"]}

- Type: [{attacks[atc]["type"].capitalize()}](#types)
- Minimum Level: {attacks[atc]["min_lvl"]}
- Attack factor: {attacks[atc]["factor"]}
- Missing chance: {attacks[atc]["miss_chance"]}
- Attack points: {attacks[atc]["ap"]}
- Effect: {"None" if attacks[atc]["effect"] is None else f'[{eval(attacks[atc]["effect"]).c_name.capitalize()}](#{eval(attacks[atc]["effect"]).c_name.replace("_", "-")})'}
"""

    # Types
    md_str += """
## Types
Those are all the Pokete/Attack types that are present in the game with all their (in)effectivities against other types.
Type|Effective against|Ineffective against
---|---|---
"""

    for poke_type in types:
        effective = ""
        for i in types[poke_type]["effective"]:
            effective += i.capitalize()+(", " if i != types[poke_type]["effective"][-1] else "")
        ineffective = ""
        for i in types[poke_type]["ineffective"]:
            ineffective += i.capitalize()+(", " if i != types[poke_type]["ineffective"][-1] else "")
        md_str += f"{poke_type.capitalize()}|{effective}|{ineffective}\n"

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
- Can be used in fights: {"Yes" if items[item]["fn"] is not None else "No"}
"""

    # effects
    md_str += """
## Effects
Those effects can be given to a Pokete through an attack.
"""

    for effect in effects:
        md_str += effect.ret_md()

    # writing to file
    with open("wiki.md", "w+") as file:
        file.write(md_str)


def gen_pics():
    md_str = "# Example pictures\n"
    for i in sorted(os.listdir("assets/ss")):
        md_str += f"![{i}](ss/{i})\n\n"

    # writing to file
    with open("assets/pics.md", "w+") as file:
        file.write(md_str)


if __name__ == "__main__":
    print(":: Generating wiki.md...")
    gen_wiki()
    print(":: Generating pics.md...")
    gen_pics()
